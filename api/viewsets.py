from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import PaymentSerializer, PaymentRequestSerializer
from core.models import Payment
from core.tasks import send_email_task
from core.mixins import (payment_log_mixin, payment_status_mixin,
                         valid_user_provider_mixin, valid_provider_payment_mixin)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def payment_get(request, status=None):
    if request.method == 'GET':
        user_pk = request.user.pk
        provider_id = valid_user_provider_mixin(user_pk)

        payment = Payment.objects.filter(provider_id=provider_id)

        if status:
            payment = payment.filter(status=status)


        serializers = PaymentSerializer(payment, many=True)
        return Response(serializers.data)


@api_view(['GET', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def payment_request(request, pk):
    old_status = 'Disponible'
    to_status = 'Requested'
    user_pk = request.user.pk
    provider_id = valid_user_provider_mixin(user_pk)
    resp = Payment.objects.get(id_payment=pk)
    list_payment = [pk, ] if resp.provider_id == provider_id and resp.status == old_status else [None, ]
    payment_pk = list_payment[0]
    if request.method == 'GET' and provider_id:
        payment = Payment.objects.filter(pk=payment_pk)
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT' and provider_id:
        try:
            payment = Payment.objects.get(pk=payment_pk)
            payment_status_mixin(list_payment, to_status)
            payment_log_mixin(user_pk, list_payment, to_status)
            send_email_task.apply_async(kwargs={'user_pk': user_pk,
                                                'provider_id': provider_id,
                                                'list_payment': list_payment,
                                                'old_status': old_status,
                                                'to_status': to_status, })
        except:
            Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentRequestSerializer(instance=payment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
