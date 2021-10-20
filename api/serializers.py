from rest_framework import serializers
from core.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id_payment', ]