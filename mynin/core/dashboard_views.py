from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import UserProfile, Invitation, Settings
from .forms import CustomCreateUserForm, SettingsForm
from .web_scraper import balanceScraper


# *************** SETTINGS ****************#
def settings(request):
    obj = get_object_or_404(Settings, id=1)
    form = SettingsForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('settings')
    ctx = {'form': form}
    return render(request, 'settings.html', ctx)


# *************** DASHBOARD ****************#


@login_required(login_url="login")
def home(requset):
    # pocet clenov
    members_list = []
    tl_one_list = []
    members = UserProfile.objects.all()
    for m in members:
        if m.status.status == 'Clen':
            members_list.append(m)
        elif m.status.status == 'Teamleader':
            tl_one_list.append(m)
    m_count = len(members_list)
    tl_one_count = len(tl_one_list)
    all_members = len(members_list) + len(tl_one_list)
    print(all_members)
    # aktualny stav uctu
    # url = 'https://ib.fio.sk/ib/transparent?a=2301819780'  # mynin
    url = 'https://ib.fio.sk/ib/transparent?a=2502312724'  # vela riadkovy ucet
    tableData = balanceScraper(url)
    currentBalance = ''
    for v in tableData.get('Bežný zostatok'):
        currentBalance = v

    return render(requset, 'home.html', context={
        'members': members,
        'm_count': m_count,
        'tl_one_count': tl_one_count,
        'all_members': all_members,
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

    else:
        return render(request, 'access_denied.html')


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


# *************** PROJECTS ****************#

def new_project(request):
    return render(request, 'new_project.html')


def projects_in(request):
    return render(request, 'projects_in.html')


def projects_out(request):
    return render(request, 'projects_out.html')
