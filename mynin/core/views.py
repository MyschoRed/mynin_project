from django.core.mail import send_mail

from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string

from .models import User, Invitation, UserProfile, ProfileStatus
from .forms import CustomUserCreationForm, InvitationForm, CustomLoginForm, SetPasswordForm
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
            if last_login is None:
                # invormacia o tom ze ma kliknut na mail...
                print("cakaj na email")

            # klasicky login uzivatela
            elif last_login is not None:
                print("login")
                return redirect("login")
        return render(request, "welcome.html")


# *************** LOGIN ****************#
class CustomLoginView(LoginView):
    template_name = 'login.html'

    # authentication_form = CustomLoginForm

    def login(self, request, template_name):
        form = CustomLoginForm()
        if request.method == "POST":
            form = CustomLoginForm(request.POST)
            # if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            # else:
            #     print("daco zle")
        return render(request, template_name, {"form": form})


# @login_required(login_url="login")
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
    return render(request, "invitation.html", {"form": form})


def request_sended(request):
    return render(request, 'request_sended.html')


# @login_required
def requests_for_invitation(request):
    invitations = Invitation.objects.all()

    context = {
        'invitations': invitations,
    }
    return render(request, 'requests_for_invitation.html', context)


def activateEmail(request, to_email):
    messages.success(request, f'Dear <b>Menoooo</b>, please go to you email <b>{to_email}</b> inbox and click on \
        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')


# @login_required
def create_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "create_user.html", {"form": form})


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
