from codepay_project import settings
from django.contrib.auth.models import User
from core.models import PaymentLog, Payment, ProviderToProfile
from django.template.loader import render_to_string
from django.core import mail
from datetime import date



def payment_status_mixin(list_id_payment, status):
    for item in list_id_payment:
        Payment.objects.filter(id_payment=item).update(status=status)
        if status == 'Released':
            value_new = apply_discount_mixin(Payment.objects.get(id_payment=item))
            Payment.objects.filter(id_payment=item).update(value_new=value_new)


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
        if resp.provider_id == provider_id and resp.status in old_status:
            result.append(item)
    return result


def persiste_provider_payments_mixin(list_items_post):
    from core.tasks import send_email_task
    old_status = ['Requested', 'Disponible']
    dict_items = {c: v for c, v in list_items_post}
    list_payment = [v for c, v in dict_items.items() if 'payment' in c]
    for payment in list_payment:
        list_payment.clear()
        for c, v in dict_items.items():
            if c != 'csrfmiddlewaretoken':
                if c.split('_')[1] == payment:
                    if c.split('_')[0] == 'payment':
                        list_payment.append(v)
                    elif c.split('_')[0] == 'provider':
                        provider_id = v
                        user_pk = get_user_provider_mixin(provider_id)
                    elif c.split('_')[0] == 'status':
                        to_status = v
        if len(list_payment) > 0 and provider_id and to_status:
            payment_status_mixin(list_payment, to_status)
            payment_log_mixin(user_pk, list_payment, to_status)
            send_email_task.apply_async(kwargs={'user_pk': user_pk,
                                                'provider_id': provider_id,
                                                'list_payment': list_payment,
                                                'old_status': old_status,
                                                'to_status': to_status, })


def get_user_provider_mixin(provider_id):
    try:
        user = ProviderToProfile.objects.get(provider_id=provider_id)
        user = user.user_id
    except:
        user = False

    return user


def apply_discount_mixin(object):
    old_value = object.value_original
    due_date = object.due_date
    date_now = date.today()
    days_to_exp = (due_date - date_now).days
    new_value = old_value - (old_value * (((3 / 100) / 30) * days_to_exp))
    return new_value if days_to_exp > 0 else old_value


def send_mail_mixin(subject, to, template_name, context):
    """Send email"""
    from_ = settings.DEFAULT_FROM_EMAIL
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])

