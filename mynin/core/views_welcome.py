from django.shortcuts import render, redirect

from .forms import CustomCreateUserForm


# *************** WELCOME ****************#
def welcome(request):
    return render(request, "welcome/login.html")


def registration(request):
    form = CustomCreateUserForm
    if request.method == 'POST':

        form = CustomCreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    # obj = Invitation.objects.get(email=email)

    context = {"form": form}
    return render(request, 'welcome/registration.html', context)


def email_confirm(request):
    return render(request, 'welcome/email_confirm.html')
