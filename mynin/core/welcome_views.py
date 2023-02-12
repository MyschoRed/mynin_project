from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import InvitationForm
from .models import Invitation


# *************** WELCOME ****************#
def welcome(request):
    if request.method == "GET":
        return render(request, "welcome/welcome.html")
    else:
        email = request.POST.get("email")

        # ak sa email nenachadza v systeme
        if not User.objects.filter(email=email).exists():
            print("prva volba")
            return redirect("invitation")
        else:
            # email je uz registrovany
            last_login = User.objects.get(email=email).last_login

            # ak uzivatel este nebol prihlaseny
            if last_login is None:
                # invormacia o tom ze ma kliknut na mail...
                return redirect('email_confirm')

            # klasicky login uzivatela
            elif last_login is not None:
                print("login")
                return redirect("login")
        return render(request, "welcome/welcome.html")


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
            send_mail('Ziadost o pozvanie do mynini.eu', 'tu je sprava', 'neodpovedat@miso.sk', [email],
                      html_message=html)
            return redirect('request_sended')
    else:
        form = InvitationForm()
    return render(request, "welcome/invitation.html", {"form": form})


def request_sended(request):
    return render(request, 'welcome/request_sended.html')


def email_confirm(request):
    return render(request, 'welcome/email_confirm.html')

