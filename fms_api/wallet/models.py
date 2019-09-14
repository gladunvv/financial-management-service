from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import models

from datetime import datetime


class Wallet(models.Model):

    name = models.CharField(_('Wallet name'), max_length=20, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='wallets',
        on_delete=models.CASCADE
    )
    balance = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        )

    class Meta:
        ordering = ('balance',)
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def __str__(self):
        return self.name + ' Ballance: ' +  str(self.balance) + ' ' + 'RUB'

    def can_send(self, amount, type_trans):
        """Check шs a write-off operation possible"""
        if type_trans == 'Write-off':
            return (self.balance - amount) >= 0
        else:
            return True

    def trans_operation(self, amount, type_trans):
        """Transfers of funds"""
        if type_trans == 'Contribution':
            self.balance += amount
            return self.save()
        else:
            self.balance -= amount
            return self.save()


class Transaction(models.Model):

    WRITE_OFF = 'Write-off'
    CONTRIBUTION = 'Contribution'
    TYPE_TRANSACTION_CHOICES = [
        (
            CONTRIBUTION,
            'Contribution'
        ),
        (
            WRITE_OFF,
            'Write-off'
        ),
    ]

    amount = models.DecimalField(_('Transaction amount'), max_digits=7, decimal_places=2)
    date_time = models.DateTimeField(_('Transaction date'), auto_now_add=True)
    comment = models.CharField(_('User comment'), max_length=70)
    wallet = models.ForeignKey(
        Wallet,
        related_name='transactions',
        on_delete=models.CASCADE
    )
    type_trans = models.CharField(
        _('Transaction type'),
        choices=TYPE_TRANSACTION_CHOICES,
        max_length=20
    )

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ('-date_time',)

    def __str__(self):
        return '%s %s %s %s' % (
            self.type_trans,
            str(self.amount),
            'RUB',
            self.date_time.strftime("%d.%m.%Y, %H:%M:%S")
            )

    def save(self, *args, **kwargs):
        """Checking the validity of the operation"""
        has_enough_money = self.wallet.can_send(self.amount, self.type_trans)
        print(has_enough_money)
        if not has_enough_money:
            return {
                'error': _('There are not enough funds in your wallet'),
            }
        elif self.amount <= 0:
            return {
                'error': _('Attention the transaction amount must be positive'),
            }
        else:
            #Wallet balance update
            self.wallet.trans_operation(self.amount, self.type_trans)

            return super(Transaction, self).save(*args, **kwargs)
