from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


def activate_email(r, user, to_email):
    """
    Odosle email po registracii s bezpecnym a jednorazovym linkom na aktivaciu.
    """
    mail_subject = 'Aktivacia uctu mynin.sk'

    message = render_to_string('emails/registration_confirm.html', {
        'user': user.first_name,
        'domain': get_current_site(r).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if r.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, 'noreply@mynin.eu', to=[to_email])
    email.content_subtype = 'html'

    if email.send():
        messages.success(r,
                         f'Ahoj <b>{user.first_name}</b>, na emailovu schranku <b>{to_email}</b> bol odoslany email s odkazom na aktivaciu uctu. \
                          <b>Note:</b> Skontroluj aj nevyziadanu postu.')
    else:
        messages.error(r, f'Nepodarilo sa odoslat email na adresu {to_email}, skontroluj zadanu adresu.')


def recharge_credit_email(r, user, user_info, settings_data, due_date, to_email):
    """
    Odosle email s pokynmi pre zaplatenie aby mohol byt navyseny kredit uzivatela.

    """
    mail_subject = 'Dobitie kreditu na mynin.sk'

    message = render_to_string('emails/send_payment_info.html', {
        'user': user,
        'user_info': user_info,
        'settings_data': settings_data,
        'due_date': due_date,
    })
    email = EmailMessage(mail_subject, message, 'noreply@mynin.eu', to=[to_email])
    email.content_subtype = 'html'

    if email.send():
        messages.success(r, f'Ahoj <b>{user.first_name}</b>, na emailovu schranku <b>{to_email}</b> bol ododslny email s pokynmi na zaplatenie. \
         <b>Note:</b> Skontroluj aj nevyziadanu postu.')
    else:
        messages.error(r, f'Nepodarilo sa odoslat email na adresu {to_email}, skontroluj zadanu adresu.')
