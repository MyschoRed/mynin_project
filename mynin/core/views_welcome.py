from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .emails import activate_email
from .forms import CustomCreateUserForm, CustomResetPasswordForm, CustomChangePasswordForm
from .tokens import account_activation_token


def welcome(request):
    return render(request, "welcome/login.html")


def registration(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = CustomCreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            activate_email(request, user, form.cleaned_data.get('username'))
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = CustomCreateUserForm()

    ctx = {"form": form}
    return render(request, 'welcome/registration.html', ctx)


def registration_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('home')


def password_reset_request(request):
    form = CustomResetPasswordForm

    if request.method == 'POST':
        form = CustomResetPasswordForm(request.POST)
        if form.is_valid:
            user_email = request.POST.get('email')
            associated_user = get_user_model().objects.filter(Q(username=user_email)).first()
            if associated_user:
                html = render_to_string('emails/password_reset_email.html', {'email': user_email})
                send_mail('Ziadost o pozvanie do mynini.eu', 'tu je sprava', 'noreply@mynin.eu', [user_email],
                          html_message=html)
            return redirect('change_password')

    ctx = {'form': form}
    return render(request, 'welcome/password_reset.html', ctx)


def password_reset_confirm(request, uid64, token):
    return redirect('login')


def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = CustomChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                print(error)
    form = CustomChangePasswordForm(user)

    ctx = {'form': form}
    return render(request, 'welcome/change_password.html', ctx)
