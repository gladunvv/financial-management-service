from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from wallet.models import Transaction, Wallet


CREATE_USER_URL = reverse('user:create')

ALL_TRANSACTION_URL = reverse('wallet:trans_all')
CREATE_TRANSACTION_URL = reverse('wallet:trans_control')
DELETE_TRANSACTION_URL = reverse('wallet:trans_delete', kwargs={'pk': 1})


class WalletApiTests(TestCase):

    def setUp(self):
        context = {
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': 'testName',
        }
        res = self.client.post(CREATE_USER_URL, context)
        user = get_user_model().objects.get(pk=1)
        wallet = Wallet.objects.create(user=user, name='Wallet')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + res.data['token'])

    def test_transaction_contribution(self):
        context = {
            'wallet': '1',
            'amount': '999',
            'type_trans': 'Contribution',
            'comment': 'My first transaction',
        }
        res = self.client.post(CREATE_TRANSACTION_URL, context)
        wallet = Wallet.objects.get(pk=1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(wallet.balance, 999)

    def test_transaction_not_positiv_amount(self):
        context = {
            'wallet': '1',
            'amount': '-999',
            'type_trans': 'Contribution',
            'comment': 'My first transaction',
        }
        res = self.client.post(CREATE_TRANSACTION_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transaction_write_off_small_balance(self):
        context = {
            'wallet': '1',
            'amount': '999',
            'type_trans': 'Write-off',
            'comment': 'My first transaction',
        }
        res = self.client.post(CREATE_TRANSACTION_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transaction_write_off_success(self):
        context_to = {
            'wallet': '1',
            'amount': '999',
            'type_trans': 'Contribution',
            'comment': 'My first transaction',
        }
        self.client.post(CREATE_TRANSACTION_URL, context_to)

        context_from = {
            'wallet': '1',
            'amount': '333',
            'type_trans': 'Write-off',
            'comment': 'My second transaction',
        }
        self.client.post(CREATE_TRANSACTION_URL, context_from)

        wallet = Wallet.objects.get(pk=1)
        self.assertEqual(wallet.balance, 666)

    def test_transaction_all_view(self):
        context = {
            'wallet': '1',
            'amount': '999',
            'type_trans': 'Contribution',
            'comment': 'My first transaction',
        }
        for _ in range(3):
            self.client.post(CREATE_TRANSACTION_URL, context)
        res = self.client.get(ALL_TRANSACTION_URL)
        transactions = Transaction.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(transactions), 3)

    def test_create_transaction_not_wallet(self):
        context = {
            'wallet': '2',
            'amount': '999',
            'type_trans': 'Contribution',
            'comment': 'My first transaction',
        }
        res = self.client.post(CREATE_TRANSACTION_URL, context)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_transaction_not_vallid_data(self):
        context = {
            'wallet': '1',
            'amount': '999',
            'type_trans': 'Contribution',
            'comment': '',
        }
        res = self.client.post(CREATE_TRANSACTION_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transaction_delete_success(self):
        context = {
            'wallet': '1',
            'amount': '999',
            'type_trans': 'Contribution',
            'comment': 'My first transaction',
        }
        self.client.post(CREATE_TRANSACTION_URL, context)
        res = self.client.delete(DELETE_TRANSACTION_URL)
        wallet = Wallet.objects.get(pk=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(wallet.balance, 999)
