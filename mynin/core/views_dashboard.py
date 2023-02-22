import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import InviteForm
from .models import UserProfile, Invoice, Settings, Invitation
from .web_scraper import balanceScraper


# *************** DASHBOARD ****************#


def access_denied(request):
    render(request, 'access_denied.html')
@login_required(login_url="login")
def home(requset):
    # pocet clenov
    all_members = len(UserProfile.objects.all())

    # aktualny stav uctu
    url = 'https://ib.fio.sk/ib/transparent?a=2301819780'  # mynin
    # url = 'https://ib.fio.sk/ib/transparent?a=2502312724'  # vela riadkovy ucet
    tableData = balanceScraper(url)
    currentBalance = ''
    for v in tableData.get('Bežný zostatok'):
        currentBalance = v

    return render(requset, 'dashboard/home.html', context={
        'all_members': all_members,
        'tableData': tableData,
        'currentBalance': currentBalance,
    })

@login_required(login_url="login")
def my_home(request):
    user_profile = UserProfile
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            print('uzivatel ma profil')
        except UserProfile.DoesNotExist:
            print('profil uzivatela neexistuje')
            return render(request, 'dashboard/error_user_profile.html')

        credit = user_profile.credit
        pp = user_profile.primary_points
        sp = user_profile.secondary_points
        tp = user_profile.team_points
        bp = user_profile.bonus_points
        sum_points = pp + sp + tp + bp
        status = user_profile.set_status
    else:
        return redirect('access_denied')

    return render(request, 'dashboard/my_home.html', context={
        'user_profile': user_profile,
        'pp': pp,
        'sp': sp,
        'tp': tp,
        'bp': bp,
        'sum_points': sum_points,
        'status': status,
        'credit': credit,
    })

def invite(request):
    set_data = Settings.objects.get(pk=1)
    invite_price = set_data.invite_price
    if request.method == "POST":
        email = request.POST.get("email")
        invitations = Invitation.objects.filter(email=email)
        form = InviteForm(request.POST)

        if form.is_valid() and invitations.exists():
            print('emial uz bol odoslany')
            return redirect('invite_sended')
        else:
            if request.user.userprofile.credit >= invite_price:
                form.save()
                request.user.userprofile.credit = request.user.userprofile.credit - invite_price
                request.user.userprofile.registrations += 1
                request.user.userprofile.save()
                html = render_to_string('emails/send_invite.html', {'email': email})
                send_mail('Ziadost o pozvanie do mynini.eu', 'tu je sprava', 'noreply@mynin.eu', [email],
                          html_message=html)
                return redirect('request_sended')
            else:
                return redirect('low_credit')
    else:
        form = InviteForm()
    return render(request, 'dashboard/invite.html', {"form": form, 'invite_price': invite_price})


def invite_sended(request):
    return render(request, 'dashboard/invite_sended.html')


def request_sended(request):
    return render(request, 'dashboard/request_sended.html')

def recharge_credit(request):
    if request.method == 'POST':
        email = request.user.username
        credit = request.POST.get('credit')
        if credit == 'other':
            choice = request.POST.get('other')
        else:
            choice = request.POST.get('credit')
        request.user.userprofile.credit_for_recharge = float(choice)
        request.user.userprofile.save()
        html = render_to_string('emails/send_payment_info.html', {'email': email})
        send_mail('Ziadost o pozvanie do mynini.eu', 'tu je sprava', 'noreply@mynin.eu', [email],
                  html_message=html)
        return redirect('recharge_confirm')

    return render(request, 'dashboard/recharge_credit.html')


def recharge_confirm(request):
    user_info = get_object_or_404(UserProfile, id=request.user.pk)
    invoice = Invoice()
    settings_data = get_object_or_404(Settings, id=1)

    d = int(settings_data.due_date)
    due_date = datetime.date.today() + datetime.timedelta(days=d)
    due_date.strftime('%d-%m-%Y')

    invoice.user_info = request.user.userprofile
    invoice.payment_info = settings_data
    invoice.value = request.user.userprofile.credit_for_recharge
    invoice.due_date = due_date
    invoice.save()

    ctx = {
        'user_info': user_info,
        'settings': settings_data,
        'due_date': due_date
    }
    return render(request, 'dashboard/recharge_confirm.html', ctx)



