import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .emails import recharge_credit_email
from .forms import InviteForm, CustomUserChangeForm
from .models import UserProfile, Invoice, Settings, Invitation, CustomUser
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
    inviter = request.user
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            print('uzivatel ma profil')
        except UserProfile.DoesNotExist:
            print('profil uzivatela neexistuje')
            return render(request, 'dashboard/error_user_profile.html')

        if request.method == "POST":
            email = request.POST.get("email")
            invitations = Invitation.objects.filter(email=email)
            user = CustomUser.objects.filter(email=email)
            form = InviteForm(request.POST)

            if form.is_valid() and invitations.exists():
                return redirect('error_invite_sended')
            elif user:
                return redirect('error_account_exists')
            else:
                if request.user.userprofile.credit >= invite_price:
                    Invitation.inviter = request.user
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
        print(inviter)
        ctx = {
            "form": form,
            'invite_price': invite_price,
            'inviter': inviter,
        }
        return render(request, 'dashboard/invite.html', ctx)


def error_invite_sended(request):
    return render(request, 'dashboard/error_invite_sended.html')


def error_account_exists(r):
    return render(r, 'dashboard/error_account_exists.html')


def request_sended(request):
    return render(request, 'dashboard/request_sended.html')


def recharge_credit(request):
    """
    Po vypleni ziadosti odosle email s pokynmi na uhradu.
    !!!
    Treba domysliet ci moze uzivatel poslat viac ziadosti o dobitie kreditu.
    Ci moze byt viac ziadosti nepotvrdenych...Vtedy NEBUDE
    fungovat docasna premenna "credit_for_recharge"
    !!!
    """
    if request.method == 'POST':
        email = request.user.username
        credit = request.POST.get('credit')
        user_info = get_object_or_404(UserProfile, id=request.user.pk)
        settings_data = get_object_or_404(Settings, id=1)

        if credit == 'other':
            choice = request.POST.get('other')
        else:
            choice = request.POST.get('credit')

        request.user.userprofile.credit_for_recharge = float(choice)
        request.user.userprofile.save()

        d = int(settings_data.due_date)
        due_date = datetime.date.today() + datetime.timedelta(days=d)
        due_date.strftime('%d-%m-%Y')

        recharge_credit_email(request, request.user, user_info, settings_data, due_date, email)

        return redirect('recharge_confirm')

    return render(request, 'dashboard/recharge_credit.html')


def recharge_confirm(request):
    user_info = get_object_or_404(UserProfile, id=request.user.pk)
    invoice = Invoice()
    settings_data = get_object_or_404(Settings, id=1)
    print(settings_data.bank_account)
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


def edit_user_profile_view(request):
    user = get_object_or_404(CustomUser, id=request.user.pk)
    form = CustomUserChangeForm(instance=user)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('edit_user_profile')


    ctx = {'form': form}
    return render(request, 'dashboard/edit_user_profile.html', ctx)
