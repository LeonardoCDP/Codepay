from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Payment, ProviderToProfile
from core.mixins import payment_log_mixin, payment_status_mixin
from core.tasks import send_email_task, hello, sum


@login_required
def index(request):
    template_name = 'index.html'
    hello.apply_async()
    return render(request, template_name)


@login_required
def rpa(request):
    user = request.user
    try:
        provider = ProviderToProfile.objects.get(user_id=user.pk)
    except:
        provider = False
    list_payment = []
    lista = {}
    old_status = 'Disponible'
    status = 'Requested'
    if request.method == 'POST' and provider:
        list_payment.clear()
        dic_items = {k: v for k, v in request.POST.items()}
        for c, v in dic_items.items():
            if 'payment' in c:
                payment_status_mixin(v)
                payment_log_mixin(v, user.pk, status)
                list_payment.append(v)
        if len(list_payment) > 0:
            user_pk = user.pk
            provider_pk = provider.provider_id

            send_email_task.apply_async(kwargs={'user_pk': user_pk,
                                                'provider_pk': provider_pk,
                                                'list_payment': list_payment,
                                                'old_status': old_status,
                                                'status': status, })

    if provider:
        lista = Payment.objects.filter(provider_id=provider.provider_id)
    response = {
        'lista': lista
    }

    template_name = 'rpa.html'
    return render(request, template_name, response)
