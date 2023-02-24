import datetime

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import SettingsForm, CustomCreateUserForm
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


def activate_user_account(request, pk):
    user = get_object_or_404(CustomUser, id=pk)

    if request.method == "POST":
        user.has_profile = True
        user.save()

        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save(user)
        return redirect('user_list')

    return render(request, 'administration/activate_user_account.html')


def request_delete(request, pk):
    obj = get_object_or_404(Invitation, id=pk)

    if request.method == "POST":
        obj.delete()
        return redirect('requests_for_invitation')

    return render(request, 'administration/request_delete.html')


def low_credit(request):
    return render(request, 'administration/low_credit.html')


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
        return redirect('credit_administration')

    return render(request, 'administration/add_credit.html')
