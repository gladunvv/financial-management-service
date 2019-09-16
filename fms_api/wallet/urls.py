from django.urls import path

from wallet.views import (
    OneWalletView,
    AllWalletView,
    CreateWalletView,
    AllTransactionView,
    CreateTransactionView,
    DeleteTransactionView,
)


app_name = 'wallet'
urlpatterns = [
    path('<int:pk>', OneWalletView.as_view(), name='wallet_pk'),
    path('all/', AllWalletView.as_view(), name='wallet_all'),
    path('create/', CreateWalletView.as_view(), name='wallet_create'),
    path('transaction/all/', AllTransactionView.as_view(), name='trans_all'),
    path('transaction/create/', CreateTransactionView.as_view(), name='trans_control'),
    path('transaction/delete/<int:pk>', DeleteTransactionView.as_view(), name='trans_delete')
]
