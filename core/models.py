from django.db import models
from utils.models import Base
from django.contrib.auth.models import User


class Profile(Base):
    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "perfil do usuário {}".format(self.user)


class Provider(Base):
    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

    register = models.CharField('CNPJ', max_length=14, primary_key=True)
    name = models.CharField('Nome da Empresa', max_length=100)
    address = models.CharField('Endereço', max_length=100)
    email_address = models.EmailField('E-mail', max_length=100)


class Payment(Base):
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    status_choices = (
        ('Disponible', 'Disponible'),
        ('Not_Disponible', 'Not_Disponible'),
        ('Requested', 'Requested'),
        ('Released', 'Released'),
        ('Denied', 'Denied'),
    )

    id_payment = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE, verbose_name='Fornecedor')
    due_date = models.DateField('Data de vencimento')
    value_original = models.FloatField('Valor original', max_length=30)
    value_new = models.FloatField('Novo Valor', max_length=30)
    status = models.CharField(max_length=14, choices=status_choices, default='Disponible')


class ProviderToProfile(models.Model):
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE)


class PaymentLog(Base):
    class Meta:
        verbose_name = 'Log de Pagamento'
        verbose_name_plural = 'Logs de Pagamentos'

    user_id = models.ForeignKey(User, models.DO_NOTHING, related_name='logs')
    payment_id = models.ForeignKey(Payment, models.DO_NOTHING)
    status = models.CharField('Status', max_length=50)

