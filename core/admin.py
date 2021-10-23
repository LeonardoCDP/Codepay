from django.contrib import admin
from core.models import Payment, Provider, PaymentLog


@admin.register(Payment)
class ModelPaymentAdmin(admin.ModelAdmin):
    list_display = ('id_payment', 'id_provider', 'due_date', 'original_value', 'status')


@admin.register(Provider)
class ModelProviderAdmin(admin.ModelAdmin):
    list_display = ('id_register', 'name', 'address', 'email')


@admin.register(PaymentLog)
class ModelPaymentLogAdmin(admin.ModelAdmin):
    list_display = ('id_payment', 'user_agent', 'status')

    '''def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False'''