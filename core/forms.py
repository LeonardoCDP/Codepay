from django import forms
from core.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
