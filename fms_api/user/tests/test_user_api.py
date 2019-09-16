from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

from django.urls import reverse


CREATE_USER_URL = reverse('user:create')
LOGIN_USER_URL = reverse('user:login')
LOGOUT_USER_URL = reverse('user:logout')
DELETE_USER_URL = reverse('user:delete')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        context = {
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': 'testName',
        }
        res = self.client.post(CREATE_USER_URL, context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_exists(self):
        context = {
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': '',
        }
        res = self.client.post(CREATE_USER_URL, context)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        context = {
            'email': 'test@twix.com',
            'password': '123',
            'username': 'testName',
        }
        res = self.client.post(CREATE_USER_URL, context)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=context['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        context = {
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': 'testName',
        }

        res = self.client.post(CREATE_USER_URL, context)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        context = {
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': 'testName',
        }
        create_user(**context)
        res = self.client.post(LOGIN_USER_URL, context)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_when_user_login(self):
        context = {
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': 'testName',
        }
        create_user(**context)
        res = self.client.post(LOGIN_USER_URL, context)
        self.assertIn('token', res.data)

    def test_user_logout(self):
        context = {
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': 'testName',
        }
        user = self.client.post(CREATE_USER_URL, context)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.data['token'])
        res = self.client.post(LOGOUT_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        context = {
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': 'testName',
        }
        user = self.client.post(CREATE_USER_URL, context)

        res = get_user_model().objects.get(username='testName')
        self.assertTrue(res)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.data['token'])
        self.client.delete(DELETE_USER_URL)

        res = get_user_model().objects.filter(username='testName')
        self.assertFalse(res)

    def test_create_more_then_one_user(self):
        context = [{
            'email': 'test@twix.com',
            'password': 'testpass',
            'username': 'testName',
        }, {
            'email': 'test@snikers.com',
            'password': 'testpass',
            'username': 'testNameNew',
        }
        ]
        for data in context:
            self.client.post(CREATE_USER_URL, data)

        user = get_user_model().objects.all()

        self.assertEqual(len(user), 1)
