from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Payment
from core.mixins import (payment_log_mixin, payment_status_mixin,
                         valid_user_provider_mixin, valid_provider_payment_mixin)
from core.tasks import send_email_task, hello, sum


@login_required
def index(request):
    template_name = 'index.html'
    hello.apply_async()
    return render(request, template_name)


@login_required
def rpa(request):
    list_result = {}
    template_name = 'rpa.html'
    old_status = 'Disponible'
    to_status = 'Requested'
    item_name = 'payment'
    user_pk = request.user.pk
    provider_id = valid_user_provider_mixin(user_pk)
    list_payment = valid_provider_payment_mixin(item_name,
                                                provider_id,
                                                request.POST.items(),
                                                old_status)

    if request.method == 'POST' and provider_id and len(list_payment) > 0:
        payment_status_mixin(list_payment, to_status)
        payment_log_mixin(user_pk, list_payment, to_status)
        send_email_task.apply_async(kwargs={'user_pk': user_pk,
                                            'provider_id': provider_id,
                                            'list_payment': list_payment,
                                            'old_status': old_status,
                                            'to_status': to_status, })

    if provider_id:
        list_result = Payment.objects.filter(provider_id=provider_id)
    response = {
        'list_result': list_result
    }
    return render(request, template_name, response)
