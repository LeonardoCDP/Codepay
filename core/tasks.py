from django.contrib.auth.models import User
from core.models import Payment, Provider
from codepay_project.celery import app
from datetime import date
from core.mixins import (send_mail_mixin, payment_log_mixin,
                         payment_status_mixin)#, get_user_provider_mixin)


@app.task(bind=True)
def send_email_task(self, *args, **kwargs):
    user_pk = kwargs.get('user_pk')
    provider_id = kwargs.get('provider_id')
    list_payment = kwargs.get('list_payment')
    old_status = kwargs.get('old_status')
    to_status = kwargs.get('to_status')
    if user_pk == None:
        user_pk, provider_id, list_payment, old_status, to_status = kwargs.get('kwargs').values()

    user = User.objects.get(pk=user_pk)
    provider = Provider.objects.get(pk=provider_id)

    payment_log_mixin(user_pk, list_payment, 'Send_email')

    subject = 'Update Status Payment'
    to = provider.email_address
    template_name = 'send_email/update_status.html'
    context = {'name': user.first_name, 'employer': provider.name, 'lista': list_payment,
               'old_status': old_status, 'to_status': to_status}

    send_mail_mixin(subject, to, template_name, context)
    return True

'''
@app.task(bind=True)
def not_disponible_task(self):
    to_status = 'Not_Disponible'
    list_payment = list()
    status = ['Disponible', 'Requested']

    date_now = date.today()
    payment = Payment.objects.all().filter(due_date=date_now).values()

    for item in payment:
        list_payment.clear()
        old_status = item['status']
        provider_id = item['provider_id']
        user_pk = get_user_provider_mixin(provider_id)
        list_payment.append(item['id_payment'])
        if old_status in status:
            payment_status_mixin(list_payment, to_status)
            payment_log_mixin(user_pk, list_payment, to_status)
            send_email_task(kwargs={'user_pk': user_pk,
                                    'provider_id': provider_id,
                                    'list_payment': list_payment,
                                    'old_status': old_status,
                                    'to_status': to_status, })

'''
@app.task(bind=True)
def hello(self):
    print('hello')
    return True


@app.task()
def sum(a, b):
    return a + b
