from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(
        queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
        queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):

        if not User.objects.all().exclude(is_superuser=True):
            user = User.objects.create_user(
                validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
            )
        else:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
