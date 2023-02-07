from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/home/', views.home, name='home'),
    path('dashboard/my_home/', views.my_home, name='my_home'),
    path("accounts/", include("django.contrib.auth.urls")),
    # path('login/', views.login, name='login'),
    # path('login/', include('django.contrib.auth.urls')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('invitation/', views.invitation, name='invitation'),
    path('create_user/', views.create_user, name='create_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('request_sended/', views.request_sended, name='request_sended'),
    path('requests_for_invitation/', views.requests_for_invitation, name='requests_for_invitation'),
]
