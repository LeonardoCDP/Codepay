from django.contrib import admin
from core.models import Payment, Provider, ProviderToProfile, PaymentLog


@admin.register(Payment)
class ModelPaymentAdmin(admin.ModelAdmin):
    list_display = ('id_payment', 'provider', 'due_date', 'value_original', 'status')


@admin.register(Provider)
class ModelProviderAdmin(admin.ModelAdmin):
    list_display = ('register', 'name', 'address', 'email_address')


@admin.register(ProviderToProfile)
class ModelProvidorToProfileAdmin(admin.ModelAdmin):
    list_display = ('provider', 'user')


@admin.register(PaymentLog)
class ModelPaymentLogAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'payment_id', 'status')

    '''def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False'''