from django import forms
from django.contrib.auth.models import User

from .models import Invitation, Settings, CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


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
    mobile = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Telefonne cislo'}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Adresa'}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mesto'}))
    postal_code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'PSC'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Heslo', }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Zopakuj heslo', }))

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'mobile',
            'address',
            'city',
            'postal_code',
            'password1',
            'password2',
        ]

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'mobile',
            'address',
            'city',
            'postal_code',
        ]

class InviteForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = Invitation
        fields = ["email"]
