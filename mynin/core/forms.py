from django import forms
from django.contrib.auth.models import User

from .models import Invitation, Settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SettingsForm(forms.ModelForm):
    invite_price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Cena pozvanky'}))
    bank_account = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Cislo uctu'}))
    due_date = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Splatnost'}))
    company_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nazov firmy'}))
    ico = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ICO'}))
    dic = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'DIC'}))
    ic_dph = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'IC DPH'}))

    class Meta:
        model = Settings
        fields = '__all__'

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
