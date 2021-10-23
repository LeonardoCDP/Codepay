import gettext

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from core.models import Payment
from core.mixins import (payment_log_mixin, payment_status_mixin,
                          valid_provider_payment_mixin)
                         #persiste_provider_payments_mixin, valid_user_provider_mixin)
from core.tasks import send_email_task
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from core.forms import PaymentForm


#index = ListView.as_view(template_name='index.html', model=Payment)


@login_required
def index(request):
    template_name = 'index.html'
    return render(request, template_name)

@login_required
def rpa(request):

    template_name = 'rpa.html'

    response = {
        'object_list': Payment.objects.all()
    }
    return render(request, template_name, response)


'''class index(ListView):
    model = Payment
    template_name = 'index.html'

    def get_queryset(self):
        return Payment.objects.filter(id_user=self.request.user.pk)'''


'''class index(UpdateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.all()
        return context'''



'''@login_required
def index(request):
    template_name = 'index.html'
    return render(request, template_name)'''


'''@login_required
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
    return render(request, template_name, response)'''


@login_required
@permission_required('global_permissions.can_acess_all_payments')
def rpa_adm(request):
    template_name = 'rpa_adm.html'


    #if request.method == 'POST':
    #    persiste_provider_payments_mixin(request.POST.items())

    list_result = Payment.objects.all()
    response = {
        'list_result': list_result
    }
    return render(request, template_name, response)
