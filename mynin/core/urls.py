from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .forms import CustomLoginForm

urlpatterns = [
    # path('', views.welcome, name='welcome'),
    path('dashboard/settings/', views.settings, name='settings'),
    path('registration/', views.new_registration, name='registration'),
    path('email_confirm/', views.email_confirm, name='email_confirm'),
    path('', LoginView.as_view(template_name="welcome/login.html", authentication_form=CustomLoginForm),
         name='login'),

    path('dashboard/', views.home, name='home'),
    path('dashboard/home/', views.home, name='home'),
    path('dashboard/my_home/', views.my_home, name='my_home'),
    path('dashboard/create_user/', views.CreateUserView.as_view(), name='create_user'),

    path('dashboard/new_project/', views.new_project, name='new_project'),
    path('dashboard/projects_in/', views.projects_in, name='projects_in'),
    path('dashboard/projects_out/', views.projects_out, name='projects_out'),

    path('dashboard/invite/', views.invite, name='invite'),
    path('dashboard/invite_sended/', views.invite_sended, name='invite_sended'),
    path('dashboard/request_sended/', views.request_sended, name='request_sended'),
    path('dashboard/low_credit/', views.low_credit, name='low_credit'),
    path('dashboard/user_list/', views.UserListView.as_view(), name='user_list'),

    path('requests_for_invitation/', views.requests_for_invitation, name='requests_for_invitation'),
    path('request_delete/<pk>', views.request_delete, name='request_delete'),

]
