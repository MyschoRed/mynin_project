from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import UserProfile
from .web_scraper import balanceScraper


# *************** DASHBOARD ****************#


def access_denied(request):
    render(request, 'access_denied.html')
@login_required(login_url="login")
def home(requset):
    # pocet clenov
    all_members = len(UserProfile.objects.all())

    # aktualny stav uctu
    url = 'https://ib.fio.sk/ib/transparent?a=2301819780'  # mynin
    # url = 'https://ib.fio.sk/ib/transparent?a=2502312724'  # vela riadkovy ucet
    tableData = balanceScraper(url)
    currentBalance = ''
    for v in tableData.get('Bežný zostatok'):
        currentBalance = v

    return render(requset, 'dashboard/home.html', context={
        'all_members': all_members,
        'tableData': tableData,
        'currentBalance': currentBalance,
    })

@login_required(login_url="login")
def my_home(request):
    user_profile = UserProfile
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            print('uzivatel ma profil')
        except UserProfile.DoesNotExist:
            print('profil uzivatela neexistuje')
            return render(request, 'dashboard/error_user_profile.html')

        credit = user_profile.credit
        pp = user_profile.primary_points
        sp = user_profile.secondary_points
        tp = user_profile.team_points
        bp = user_profile.bonus_points
        sum_points = pp + sp + tp + bp
        status = user_profile.set_status
    else:
        return redirect('access_denied')

    return render(request, 'dashboard/my_home.html', context={
        'user_profile': user_profile,
        'pp': pp,
        'sp': sp,
        'tp': tp,
        'bp': bp,
        'sum_points': sum_points,
        'status': status,
        'credit': credit,
    })

