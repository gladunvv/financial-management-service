from django.contrib import admin
from wallet.models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    
    readonly_fields = ('balance',)

    list_display = ['name', 'balance']

    search_fields = ['name']

    ordering = ('balance',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ['type_trans', 'wallet', 'amount', 'date_time']

    search_fields = ['wallet']

    list_filter = ['date_time', 'type_trans', 'wallet']

    ordering = ('amount', 'date_time')
