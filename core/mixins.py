from codepay_project import settings
from django.contrib.auth.models import User
from core.models import PaymentLog, Payment, Provider, ProviderToProfile
from django.template.loader import render_to_string
from django.core import mail


def payment_status_mixin(list_id_payment, status):
    for item in list_id_payment:
        Payment.objects.filter(id_payment=item).update(status=status)


def payment_log_mixin(user_pk, list_id_payment, status):
    for item in list_id_payment:
        PaymentLog.objects.create(
            user_id=User.objects.get(pk=user_pk),
            payment_id=Payment.objects.get(id_payment=item),
            status=status,
        )


def valid_user_provider_mixin(user_id):
    try:
        provider = ProviderToProfile.objects.get(user_id=user_id)
        provider = provider.provider_id
    except:
        provider = False

    return provider


def get_elements_mixin(item_name, dic_elements):
    result = []
    for c, v in dic_elements:
        if item_name in c:
            result.append(v)
    return result


def valid_provider_payment_mixin(item_name, provider_id, list_items_post, old_status):
    list_payments = get_elements_mixin(item_name, list_items_post)
    result = []
    for item in list_payments:
        try:
            resp = Payment.objects.get(id_payment=item)
        except:
            resp = None
        if resp.provider_id == provider_id and resp.status == old_status:
            result.append(item)
    return result


def get_user_provider_mixin(provider_id):
    try:
        user = ProviderToProfile.objects.get(provider_id=provider_id)
        user = user.user_id
    except:
        user = False

    return user


def send_mail_mixin(subject, to, template_name, context):
    """Send email"""
    from_ = settings.DEFAULT_FROM_EMAIL
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])

