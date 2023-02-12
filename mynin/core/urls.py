from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .forms import CustomLoginForm

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('email_confirm/', views.email_confirm, name='email_confirm'),
    path('invitation/', views.invitation, name='invitation'),
    path('request_sended/', views.request_sended, name='request_sended'),
    path('login/', LoginView.as_view(template_name="welcome/login.html", authentication_form=CustomLoginForm),
         name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/home/', views.home, name='home'),
    path('dashboard/my_home/', views.my_home, name='my_home'),
    path('dashboard/create_user', views.CreateUserView.as_view(), name='create_user'),

    path('registration/', views.new_registration, name='registration'),
    path('requests_for_invitation/', views.requests_for_invitation, name='requests_for_invitation'),
    path('request_delete/<pk>', views.request_delete, name='request_delete'),

]
