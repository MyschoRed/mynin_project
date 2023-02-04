from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("accounts/", include("django.contrib.auth.urls")),
    # path('login/', views.login, name='login'),
    path('login/', views.CustomLogin.as_view(), name='login'),
    path('invitation/', views.invitation, name='invitation'),
    path('create_user/', views.create_user, name='create_user'),
    path('change_password/', views.change_password, name='change_password'),
]