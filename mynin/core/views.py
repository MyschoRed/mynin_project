from django.core.mail import send_mail

from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .models import Invitation, UserProfile, ProfileStatus
from .forms import InvitationForm
from .web_scraper import balanceScraper


def home(requset):
    # pocet clenov
    members_list = []
    tl_one_list = []
    members = UserProfile.objects.all()
    for m in members:
        if m.status.status == 'Clen':
            members_list.append(m)
        elif m.status.status == 'Teamleader I':
            tl_one_list.append(m)
    m_count = len(members_list)
    tl_one_count = len(tl_one_list)

    # aktualny stav uctu
    url = 'https://ib.fio.sk/ib/transparent?a=2301819780'  # mynin
    # url = 'https://ib.fio.sk/ib/transparent?a=2502312724'  # vela riadkovy ucet
    tableData = balanceScraper(url)
    currentBalance = ''
    for v in tableData.get('Bežný zostatok'):
        currentBalance = v

    return render(requset, 'home.html', context={
        'members': members,
        'm_count': m_count,
        'tl_one_count': tl_one_count,
        'tableData': tableData,
        'currentBalance': currentBalance,
    })


def my_home(request):
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            print('profil neexistuje')

        pp = user_profile.primary_points
        sp = user_profile.secondary_points
        tp = user_profile.team_points
        bp = user_profile.bonus_points
        sum_points = pp + sp + tp + bp
        status = user_profile.status

    return render(request, 'my_home.html', context={
        'pp': pp,
        'sp': sp,
        'tp': tp,
        'bp': bp,
        'sum_points': sum_points,
        'status': status,
    })


# *************** WELCOME ****************#
def welcome(request):
    if request.method == "GET":
        return render(request, "welcome/welcome.html")
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
            if last_login is None:
                # invormacia o tom ze ma kliknut na mail...
                return redirect('email_confirm')

            # klasicky login uzivatela
            elif last_login is not None:
                print("login")
                return redirect("login")
        return render(request, "welcome/welcome.html")



# *************** LOGIN ****************#



@login_required(login_url="login")
def dashboard(request):
    context = {

    }
    return render(request, 'dashboard.html', context)


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

@login_required
def requests_for_invitation(request):
    invitations = Invitation.objects.all()

    context = {
        'invitations': invitations,
    }
    return render(request, 'requests_for_invitation.html', context)


# @login_required
# def registration(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, "registration/registration.html", {"form": form})


# @login_required
# def change_password(request):
#     # user = request.user
#     email = request.POST.get("email")
#     if request.method == "POST":
#         email = request.POST.get("email")
#         form = SetPasswordForm(email, request.POST)
#         # return render(request, 'change_password.html')
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your password has been changed")
#             return redirect("login")
#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)
#             print(messages)
#
#     form = SetPasswordForm(email)
#     return render(request, "change_password.html", {"form": form})
