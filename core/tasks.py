from django.contrib.auth.models import User
from core.mixins import send_mail_mixin, payment_log_mixin
from core.models import Payment, Provider
from codepay_project.celery import app


@app.task(bind=True)
def send_email_task(self, *args, **kwargs):
    user_pk, provider_pk, list_payment, old_status, to_status = kwargs.get('kwargs').values()

    user = User.objects.get(pk=user_pk)
    provider = Provider.objects.get(pk=provider_pk)

    for id in list_payment:
        payment_log_mixin(id, user_pk, 'Send_email')

    subject = 'Update Status Payment'
    to = provider.email_address
    template_name = 'send_email/update_status.html'
    context = {'name': user.first_name, 'employer': provider.name, 'lista': list_payment,
               'old_status': old_status, 'to_status': to_status}

    send_mail_mixin(subject, to, template_name, context)
    return True


@app.task(bind=True)
def hello(self):
    print('hello')
    return True


@app.task()
def sum(a, b):
    return a + b
