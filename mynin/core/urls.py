from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .forms import CustomLoginForm

urlpatterns = [
    path('access_denied/', views.access_denied, name='access_denied'),

    path('', LoginView.as_view(template_name="welcome/login.html", authentication_form=CustomLoginForm),
         name='login'),
    path('welcome/registration/', views.registration, name='registration'),
    path('welcome/email_confirm/', views.email_confirm, name='email_confirm'),

    path('dashboard/', views.home, name='home'),
    path('dashboard/home/', views.home, name='home'),
    path('dashboard/my_home/', views.my_home, name='my_home'),
    path('dashboard/recharge_credit/', views.recharge_credit, name='recharge_credit'),
    path('dashboard/recharge_confirm/', views.recharge_confirm, name='recharge_confirm'),
    path('dashboard/invite/', views.invite, name='invite'),
    path('dashboard/request_sended/', views.request_sended, name='request_sended'),
    path('dashboard/invite_sended/', views.error_invite_sended, name='error_invite_sended'),
    path('dashboard/account_exists/', views.error_account_exists, name='error_account_exists'),

    path('projects/new_project/', views.new_project, name='new_project'),
    path('projects/projects_in/', views.projects_in, name='projects_in'),
    path('projects/projects_out/', views.projects_out, name='projects_out'),

    path('administraton/create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('administraton/low_credit/', views.low_credit, name='low_credit'),
    path('administraton/user_list/', views.UserListView.as_view(), name='user_list'),
    path('administraton/activate_user_account/<pk>', views.activate_user_account, name='activate_user_account'),
    path('administraton/settings/', views.settings, name='settings'),

    path('administraton/requests_for_invitation/', views.requests_for_invitation, name='requests_for_invitation'),
    path('administraton/request_delete/<pk>', views.request_delete, name='request_delete'),
    path('administraton/credit_administration/', views.credit_administration, name='credit_administration'),
    path('administraton/add_credit/<pk>', views.add_credit, name='add_credit'),

]
