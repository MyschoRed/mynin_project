from django.urls import path
from django.contrib.auth.views import LoginView
from . import views_welcome, views_dashboard, views_administration, views_projects
from .forms import CustomLoginForm

urlpatterns = [
    path('access_denied/', views_dashboard.access_denied, name='access_denied'),
    path('login/', LoginView.as_view(template_name="welcome/login.html", authentication_form=CustomLoginForm),
         name='login'),
    path('welcome/password_reset/', views_welcome.password_reset_request, name='password_reset_request'),
    path('reset/<uid64>/<token>', views_welcome.password_reset_confirm, name='password_reset_confirm'),
    path('welcome/password_change/', views_welcome.password_change, name='password_change'),
    path('registration/', views_welcome.registration, name='registration'),
    path('registration_confirm/<uidb64>/<token>', views_welcome.registration_confirm, name='registration_confirm'),
    path('edit_user_profile/', views_dashboard.edit_user_profile_view, name='edit_user_profile'),
    path('', views_dashboard.home, name='home'),
    path('dashboard/home/', views_dashboard.home, name='home'),
    path('dashboard/my_home/', views_dashboard.my_home, name='my_home'),
    path('dashboard/recharge_credit/', views_dashboard.recharge_credit, name='recharge_credit'),
    path('dashboard/recharge_confirm/', views_dashboard.recharge_confirm, name='recharge_confirm'),
    path('dashboard/invite/', views_dashboard.invite, name='invite'),
    path('dashboard/request_sended/', views_dashboard.request_sended, name='request_sended'),
    path('dashboard/invite_sended/', views_dashboard.error_invite_sended, name='error_invite_sended'),
    path('dashboard/account_exists/', views_dashboard.error_account_exists, name='error_account_exists'),

    path('projects/new_project/', views_projects.new_project, name='new_project'),
    path('projects/projects_in/', views_projects.projects_in, name='projects_in'),
    path('projects/projects_out/', views_projects.projects_out, name='projects_out'),

    path('administraton/create_user/', views_administration.CreateUserView.as_view(), name='create_user'),
    path('administraton/low_credit/', views_administration.low_credit, name='low_credit'),
    path('administraton/user_list/', views_administration.UserListView.as_view(), name='user_list'),
    path('administraton/activate_user_account/<pk>', views_administration.activate_user_account,
         name='activate_user_account'),
    path('administraton/settings/', views_administration.settings, name='settings'),

    path('administraton/requests_for_invitation/', views_administration.requests_for_invitation,
         name='requests_for_invitation'),
    path('administraton/request_delete/<pk>', views_administration.request_delete, name='request_delete'),
    path('administraton/credit_administration/', views_administration.credit_administration,
         name='credit_administration'),
    path('administraton/add_credit/<pk>', views_administration.add_credit, name='add_credit'),

]
