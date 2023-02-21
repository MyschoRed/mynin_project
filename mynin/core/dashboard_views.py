import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import UserProfile, Invitation, Settings, CustomUser, Invoice
from .forms import CustomCreateUserForm, SettingsForm, InviteForm, RechargeCreditForm
from .web_scraper import balanceScraper


# *************** ADMINISTRATION ****************#
class UserListView(ListView):
    template_name = 'user_list.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return CustomUser.objects.all()



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
    return render(request, "invite.html", {"form": form, 'invite_price': invite_price})


def invite_sended(request):
    return render(request, 'invite_sended.html')


def request_sended(request):
    return render(request, 'request_sended.html')


def low_credit(request):
    return render(request, 'low_credit.html')


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

    return render(request, 'recharge_credit.html')


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
    return render(request, 'recharge_confirm.html', ctx)

@user_passes_test(lambda user: user.is_superuser)
def requests_for_invitation(request):
    invitations = Invitation.objects.all()

    context = {
        'invitations': invitations,
    }
    return render(request, 'requests_for_invitation.html', context)

@user_passes_test(lambda user: user.is_superuser)
def credit_administration(request):
    invoices = Invoice.objects.all()

    ctx = {
        'invoices': invoices,
    }

    return render(request, 'credit_administration.html', ctx)

@user_passes_test(lambda user: user.is_superuser)
def add_credit(request, pk):
    obj = get_object_or_404(Invoice, id=pk)

    if request.method == 'POST':
        obj.user_info.credit = float(obj.user_info.credit) + float(obj.user_info.credit_for_recharge)
        obj.user_info.credit_for_recharge = 0
        obj.user_info.save()
        obj.delete()
        print('obj vymazany')
        return redirect('credit_administration')

    return render(request, 'add_credit.html')



# ________ SETTINGS ________#
def settings(request):
    obj = get_object_or_404(Settings, id=1)
    form = SettingsForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('settings')
    ctx = {'form': form}
    return render(request, 'settings.html', ctx)


# *************** DASHBOARD ****************#


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

    return render(requset, 'home.html', context={
        'all_members': all_members,
        'tableData': tableData,
        'currentBalance': currentBalance,
    })


def my_home(request):
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            print('profil neexistuje')
        credit = user_profile.credit
        pp = user_profile.primary_points
        sp = user_profile.secondary_points
        tp = user_profile.team_points
        bp = user_profile.bonus_points
        sum_points = pp + sp + tp + bp
        status = user_profile.set_status()

        return render(request, 'my_home.html', context={
            'user_profile': user_profile,
            'pp': pp,
            'sp': sp,
            'tp': tp,
            'bp': bp,
            'sum_points': sum_points,
            'status': status,
            'credit': credit,
        })

    else:
        return render(request, 'access_denied.html')


class CreateUserView(CreateView):
    form_class = CustomCreateUserForm
    success_url = reverse_lazy('requests_for_invitation')
    template_name = 'create_user.html'


def request_delete(request, pk):
    obj = get_object_or_404(Invitation, id=pk)

    if request.method == "POST":
        obj.delete()
        return redirect("requests_for_invitation")

    return render(request, "request_delete.html")


# *************** PROJECTS ****************#

def new_project(request):
    return render(request, 'new_project.html')


def projects_in(request):
    return render(request, 'projects_in.html')


def projects_out(request):
    return render(request, 'projects_out.html')
