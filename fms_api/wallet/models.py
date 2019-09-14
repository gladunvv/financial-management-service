from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _


class Wallet(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wallets', on_delete=models.CASCADE)
    name = models.CharField(_('Wallet name'), max_length=20, unique=True)
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    class Meta:
        ordering = ('balance',)
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def __str__(self):
        return self.name

    def can_send(self, amount):
        return (self.balance - amount) >= 0

    def trans_operation(self, amount, type):

        if type == 'Contribution':
            self.balance += amount
            return self.save()
        else:
            self.balance -= amount
            return self.save()


class Transaction(models.Model):

    TYPE_TRANSACTION_CHOICES = [
        (
            'WriteOff',
            'Contribution'
        ),
    ]

    amount = models.DecimalField(_('Transaction amount'), max_digits=7, decimal_places=2)
    date_time = models.DateTimeField(_('Transaction date'), auto_now_add=True)
    wallet = models.ForeignKey(
        Wallet,
        required=True,
        related_name='transactions',
        on_delete=models.CASCADE
    )
    type = models.CharField(
        choices=TYPE_TRANSACTION_CHOICES,
        required=True,
    )

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ('date_time',)

    def __str__(self):
        from_user = ' From: ' + self.from_wallet.user.username
        from_to = from_user + ' To: ' + self.to_wallet.user.username
        return str(self.amount) + from_to + ' ' + str(self.date_time)

    def save(self, *args, **kwargs):
        """Checking the validity of the operation"""
        has_enough_money = self.from_wallet.can_send(self.amount)

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
            self.wallet.trans_operation(self.amount, self.type)

            return super(Transaction, self).save(*args, **kwargs)
