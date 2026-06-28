from django.db import models
from django.conf import settings


class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('succeeded', 'Оплачен'),
        ('canceled', 'Отменен'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    payment_id = models.CharField('ID платежа YooKassa', max_length=255, unique=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    ts_created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.payment_id} ({self.user.login}) - {self.amount} руб'
