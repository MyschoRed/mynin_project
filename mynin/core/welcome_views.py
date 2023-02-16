from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import CustomCreateUserForm
from .models import Invitation


# *************** WELCOME ****************#
def welcome(request):
    # if request.method == "GET":
    #     return render(request, "welcome/welcome.html")
    # else:
    #     email = request.POST.get("email")
    #     # ak sa email nenachadza v systeme
    #     if not User.objects.filter(email=email).exists():
    #         print("prva volba")
    #         return redirect("invitation")
    #     else:
    #         # email je uz registrovany
    #         last_login = User.objects.get(email=email).last_login
    #
    #         # ak uzivatel este nebol prihlaseny
    #         if last_login is None:
    #             # invormacia o tom ze ma kliknut na mail...
    #             return redirect('email_confirm')
    #
    #         # klasicky login uzivatela
    #         elif last_login is not None:
    #             print("login")
    #             return redirect("login")
    return render(request, "welcome/login.html")

def new_registration(request):
    form = CustomCreateUserForm
    if request.method == 'POST':
        form = CustomCreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    # obj = Invitation.objects.get(email=email)

    context = {"form": form}
    return render(request, 'welcome/registration.html', context)



def email_confirm(request):
    return render(request, 'welcome/email_confirm.html')

