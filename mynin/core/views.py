from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.template.loader import render_to_string

from .models import User, Invitation
from .forms import CustomUserCreationForm, InvitationForm, CustomLoginForm, SetPasswordForm


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


#*************** LOGIN ****************#
def login(request):
    form = CustomLoginForm()
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
        else:
            print("daco zle")
    return render(request, 'login.html', {"form": form})



@login_required
def dashboard(request):

    context = {
        
    }
    return render(request, 'dashboard.html', context)

@login_required
def invitation(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        invitations = Invitation.objects.filter(email=email)
        form = InvitationForm(request.POST)

        if form.is_valid() and invitations.exists():
            print('emial uz bol odoslany')
            return redirect('login')
        else:
            form.save() 
            html = render_to_string('emails/send_invite.html', {'name': name, 'email': email, 'mobile': mobile})
            # activateEmail(request, form.cleaned_data.get('email'))
            send_mail('Ziadost o pozvanie do mynini.eu', 'tu je sprava', 'neodpovedat@miso.sk', [email], html_message=html)
            return redirect('request_sended')
    else:
        form = InvitationForm()
    return render(request, "invitation.html", {"form": form})
    

def request_sended(request):
    return render(request, 'request_sended.html')


@login_required
def requests_for_invitation(request):
    invitations = Invitation.objects.all()

    context = {
        'invitations' : invitations,
    }
    return render(request, 'requests_for_invitation.html', context)


def activateEmail(request, to_email):
    messages.success(request, f'Dear <b>Menoooo</b>, please go to you email <b>{to_email}</b> inbox and click on \
        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')


@login_required
def create_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "create_user.html", {"form": form})


@login_required
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
