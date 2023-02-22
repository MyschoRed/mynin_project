import datetime

from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import InviteForm, SettingsForm, CustomCreateUserForm
from .models import Invoice, Invitation, CustomUser, Settings, UserProfile


# *************** SETTINGS ****************#
def settings(request):
    obj = get_object_or_404(Settings, id=1)
    form = SettingsForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('settings')
    ctx = {'form': form}
    return render(request, 'administration/settings.html', ctx)


# *************** ADMINISTRATION ****************#

class CreateUserView(CreateView):
    form_class = CustomCreateUserForm
    success_url = reverse_lazy('requests_for_invitation')
    template_name = 'dashboard/create_user.html'


class UserListView(ListView):
    template_name = 'administration/user_list.html'
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
    return render(request, 'administration/invite.html', {"form": form, 'invite_price': invite_price})


def invite_sended(request):
    return render(request, 'administration/invite_sended.html')


def request_sended(request):
    return render(request, 'administration/request_sended.html')


def request_delete(request, pk):
    obj = get_object_or_404(Invitation, id=pk)

    if request.method == "POST":
        obj.delete()
        return redirect('requests_for_invitation')

    return render(request, 'administration/request_delete.html')


def low_credit(request):
    return render(request, 'administration/low_credit.html')


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

    return render(request, 'administration/recharge_credit.html')


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
    return render(request, 'administration/recharge_confirm.html', ctx)


@user_passes_test(lambda user: user.is_superuser)
def requests_for_invitation(request):
    invitations = Invitation.objects.all()

    context = {
        'invitations': invitations,
    }
    return render(request, 'administration/requests_for_invitation.html', context)


@user_passes_test(lambda user: user.is_superuser)
def credit_administration(request):
    invoices = Invoice.objects.all()

    ctx = {
        'invoices': invoices,
    }

    return render(request, 'administration/credit_administration.html', ctx)


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

    return render(request, 'administration/add_credit.html')
