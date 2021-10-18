from django.test import TestCase
from core.models import Payment, Provider


class ModelPaymentTest(TestCase):
    def setUp(self):
        obj_provider = Provider.objects.create(register='11122233000120',
                                               name='Jose Silva LTDA',
                                               address='Umuarama, 250',
                                               email_address='Carlos@JoseSilva.com.br')

        self.obj = Payment.objects.create(provider=obj_provider,
                                     due_date='2021-10-11',
                                     value_original='1000.00',
                                     status='')
        obj_provider.save()
        self.obj.save()

        self.assertTrue(Payment.objects.exists())

    def test_get(self):
        pass
