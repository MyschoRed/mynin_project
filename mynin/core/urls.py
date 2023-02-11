from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .forms import CustomLoginForm


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('email_confirm/', views.email_confirm, name='email_confirm'),
    path('invitation/', views.invitation, name='invitation'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/home/', views.home, name='home'),
    path('dashboard/my_home/', views.my_home, name='my_home'),
    path('login/', LoginView.as_view(template_name="welcome/login.html",
                                     authentication_form=CustomLoginForm), name='login'),
    # path('registration/', views.registration, name='registration'),
    # path('change_password/', views.change_password, name='change_password'),
    path('request_sended/', views.request_sended, name='request_sended'),
    path('requests_for_invitation/', views.requests_for_invitation, name='requests_for_invitation'),
]
