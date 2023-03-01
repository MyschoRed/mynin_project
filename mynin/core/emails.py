from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


def activate_email(request, user, to_email):
    mail_subject = 'Aktivacia uctu'

    message = render_to_string('emails/registration_confirm.html', {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, 'noreply@mynin.eu', to=[to_email])
    # email = send_mail(mail_subject, message, 'noreply@mynin.eu', [to_email],
    #                   html_message=message)

    if email.send():
        messages.success(request, f'Dear <b>{user.first_name}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                    received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')
