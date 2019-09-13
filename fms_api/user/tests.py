from django.test import TestCase
from django.contrib.auth.models import User
from 

class UserTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(name="lion", password="roar-roar")
        User.objects.create_superuser(name="cat", password="meow-meow")
        User.objects.create_superuser(name="dog", passowrd="woof-woof")
        User.objects.create_superuser(name="pig", password="oink-oink")
