from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import User
from .forms import CustomUserCreationForm, InvitationForm, LoginForm, SetPasswordForm


def welcome(request):
    if request.method == "GET":
        return render(request, "welcome.html")
    else:
        email = request.POST.get("email")

        # ak sa email nenachadza v systeme
        if User.objects.filter(email=email).exists() == False:
            print("prva volba")
            return redirect("invitation")
        else:

            # email je uz registrovany
            last_login = User.objects.get(email=email).last_login

            # ak uzivatel este nebol prihlaseny
            if last_login == None:
                # invormacia o tom ze ma kliknut na mail...
                print("cakaj na email")

            # klasicky login uzivatela
            elif last_login != None:
                print("login")
                return redirect("login")
        return render(request, "welcome.html")

def dashboard(request):
    return render(request, 'dashboard.html')

def invitation(request):
    form = InvitationForm()
    return render(request, "invitation.html", {"form": form})


def create_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "create_user.html", {"form": form})


class CustomLogin(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid user name or password")
        return self.render_to_response(self.get_context_data(form=form))

    def login(request):
        form = LoginForm()
        if form.is_valid():
            login(request)
            return redirect("/dashboard")
        else:
            print("daco zle")
        return render(request, "login.html", {"form": form})


# @login_required
def change_password(request):
    # user = request.user
    email = request.POST.get("email")
    if request.method == "POST":
        email = request.POST.get("email")
        form = SetPasswordForm(email, request.POST)
        # return render(request, 'change_password.html')
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect("login")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            print(messages)

    form = SetPasswordForm(email)
    return render(request, "change_password.html", {"form": form})
