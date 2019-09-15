from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from wallet.models import Transaction, Wallet


CREATE_USER_URL = reverse('user:create')

WALLET_URL = reverse('wallet:wallet_pk', kwargs={'pk': 1})
ALL_WALLET_URL = reverse('wallet:wallet_all')
CREATE_WALLET_URL = reverse('wallet:wallet_create')


class WalletApiTests(TestCase):
    
    def setUp(self):
        context = {
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': 'testName',
        }
        user = self.client.post(CREATE_USER_URL, context)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.data['token'])

    def test_create_wallet_view(self):
        context = {
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_WALLET_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_one_walled_view(self):
        context = {
            'name': 'Test Name'
        }
        self.client.post(CREATE_WALLET_URL, context)
        res = self.client.get(WALLET_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_wallet(self):
        context_create = {
            'name': 'Test Name'
        }
        self.client.post(CREATE_WALLET_URL, context_create)
        context_update = {
            'name': 'NEW NAME'
        }
        self.client.patch(WALLET_URL, context_update)
        wallet = Wallet.objects.get(pk=1)
        self.assertEqual(wallet.name, 'NEW NAME')

    def test_update_wallet_not_valid_field(self):
        context_create = {
            'name': 'Test Name'
        }
        self.client.post(CREATE_WALLET_URL, context_create)
        context_update = {
            'name': ''
        }
        res = self.client.patch(WALLET_URL, context_update)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_wallet(self):
        context = {
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_WALLET_URL, context)
        wallet = Wallet.objects.get(pk=1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(wallet.id, 1)

        res = self.client.delete(WALLET_URL)
        wallet = Wallet.objects.filter(pk=1)
        self.assertFalse(wallet)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_all_wallet_view(self):
        context = [
            {'name': 'Test one'},
            {'name': 'Test two'},
            {'name': 'Test three'},
            {'name': 'Test four'},
        ]
        res_befor = Wallet.objects.all()
        self.assertEqual(len(res_befor), 0)
        for data in context:
            self.client.post(CREATE_WALLET_URL, data)

        res_after = Wallet.objects.all()
        self.assertEqual(len(res_after), 4)

    def test_not_acess_balance(self):
        context = {
            'name': 'Test Name',
            'balance': '999'
        }
        self.client.post(CREATE_WALLET_URL, context)
        res = Wallet.objects.get(name='Test Name')
        self.assertEqual(res.balance, 0.00)
