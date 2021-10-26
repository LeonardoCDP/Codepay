from django.db import models
from utils.models import Base
from django.contrib.auth.models import User
import uuid


class Profile(Base):
    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'perfil do usuário {self.user}'


class Provider(Base):
    class Meta:
        verbose_name = 'fornecedor'
        verbose_name_plural = 'fornecedores'
        ordering = ['name']

    def __str__(self):
        """String for representing the Model Object"""
        return f'{self.name}'

    id_register = models.CharField('CNPJ', max_length=14, primary_key=True)
    id_user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Usuario')
    name = models.CharField('Nome da Empresa', max_length=100)
    address = models.CharField('Endereço', max_length=100)
    email = models.EmailField('E-mail', max_length=100)
    phone = models.CharField('Telefone', max_length=100)
    site = models.CharField('Site', max_length=100)


class Payment(Base):
    class Meta:
        verbose_name = 'pagamento'
        verbose_name_plural = 'pagamentos'
        ordering = ['due_date']

    def __str__(self):
        """String for representing the Model Object"""
        return f'{self.id_provider.name}({self.id_payment})'

    status_choices = (
        ('disponible', 'Disponible'),
        ('not_disponible', 'Not_Disponible'),
        ('requested', 'Requested'),
        ('released', 'Released'),
        ('denied', 'Denied'),
    )

    id_payment = models.UUIDField(primary_key=True, default=uuid.uuid4)
    id_provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='Fornecedor')
    due_date = models.DateField('Data de vencimento')
    original_value = models.FloatField('Valor original', max_length=30)
    new_value = models.FloatField('Novo Valor', max_length=30)
    status = models.CharField(max_length=14, choices=status_choices, default='disponible')
    doc_number = models.CharField('Numero do Boleto', max_length=255, null=True, blank=True)


class PaymentLog(Base):
    class Meta:
        verbose_name = 'log de pagamento'
        verbose_name_plural = 'logs de pagamentos'

    user_agent = models.CharField(max_length=512)
    status = models.CharField('Status', max_length=50)
    id_payment = models.ForeignKey(Payment, models.DO_NOTHING, related_name='logs')
