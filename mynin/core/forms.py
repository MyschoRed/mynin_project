from django import forms
from django.contrib.auth.models import User

from .models import Invitation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Heslo'}))


class CustomCreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomCreateUserForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Meno'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Priezvisko'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Heslo', }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Zopakuj heslo', }))

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]


class InvitationForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    mobile = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile'}))

    class Meta:
        model = Invitation
        fields = ["name", "email", "mobile"]
