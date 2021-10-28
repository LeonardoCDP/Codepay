from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import PaymentSerializer, PaymentRequestSerializer
from core.models import Payment, Provider
from core.mixins import (persiste_payments_mixin)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def payment_get(request, status=None):
    if request.method == 'GET':
        user = request.user
        provider = Provider.objects.get(id_user=user.pk)
        payment = Payment.objects.filter(id_provider=provider.pk)

        if status:
            payment = payment.filter(status=status)

        serializers = PaymentSerializer(payment, many=True)
        return Response(serializers.data)


@api_view(['GET', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def payment_request(request, hashid):
    user = request.user
    provider = Provider.objects.get(id_user=user.pk)
    dict_payment = {'payment': hashid, }
    if request.method == 'GET':
        payment = Payment.objects.get(id_payment=hashid)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        try:
            persiste_payments_mixin(user, provider, dict_payment.items())
            payment = Payment.objects.get(id_payment=hashid)
        except:
            Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentSerializer(payment)

        return Response(serializer.data)
