from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.mixins import (persiste_mult_provider_payments_mixin,
                         persiste_payments_mixin)
from core.models import Payment, Provider


@login_required
def index(request):
    template_name = 'index.html'
    return render(request, template_name)


@login_required
def rpa(request):
    template_name = 'rpa.html'
    user = request.user
    provider = Provider.objects.get(id_user=user.pk)

    if request.method == 'POST':
        persiste_payments_mixin(user, provider, request.POST.items())

    response = {
        'object_list': Payment.objects.filter(id_provider=provider.pk)
    }
    return render(request, template_name, response)


@login_required
@permission_required('global_permissions.can_acess_all_payments')
def rpa_adm(request):
    template_name = 'rpa_adm.html'

    if request.method == 'POST':
        persiste_mult_provider_payments_mixin(request.POST.items())

    response = {
        'object_list': Payment.objects.all()
    }
    return render(request, template_name, response)
