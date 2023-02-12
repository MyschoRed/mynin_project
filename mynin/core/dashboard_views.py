
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import UserProfile, Invitation
from .forms import CustomCreateUserForm
from .web_scraper import balanceScraper

# *************** DASHBOARD ****************#
@login_required(login_url="login")
def dashboard(request):
    context = {

    }
    return render(request, 'dashboard.html', context)


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


@login_required
def requests_for_invitation(request):
    invitations = Invitation.objects.all()

    context = {
        'invitations': invitations,
    }
    return render(request, 'requests_for_invitation.html', context)


class CreateUserView(CreateView):
    form_class = CustomCreateUserForm
    success_url = reverse_lazy('requests_for_invitation')
    template_name = 'create_user.html'


def new_registration(request, pk):
    obj = get_object_or_404(Invitation, id=pk)

    context = {"form": form}
    return render(request, "registration", context)


def request_delete(request, pk):
    obj = get_object_or_404(Invitation, id=pk)

    if request.method == "POST":
        obj.delete()
        return redirect("requests_for_invitation")

    return render(request, "request_delete.html")
