from codepay_project import settings
from django.contrib.auth.models import User
from core.models import PaymentLog, Payment, Profile
from django.template.loader import render_to_string
from django.core import mail


def payment_status_mixin(id_payment):
    Payment.objects.filter(id_payment=id_payment).update(status='Requested')


def payment_log_mixin(id_payment, user_pk, status):
    PaymentLog.objects.create(
        user_id=User.objects.get(pk=user_pk),
        payment_id=Payment.objects.get(id_payment=id_payment),
        status=status,
    )



def send_mail_mixin(subject, to, template_name, context):
    """Send email"""
    from_ = settings.DEFAULT_FROM_EMAIL
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])

