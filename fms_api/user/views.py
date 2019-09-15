from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from user.serializers import UserSerializer


class UserCreateView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
            return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogInView(ObtainAuthToken, APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class UserLogOutView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        msg = ('You have successfully logged out the application')
        return Response({'message': msg}, status=status.HTTP_200_OK)


class UserDeleteView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, format=None):
        request.user.delete()
        msg = ('Your account has been successfully deleted')
        return Response({'message': msg}, status=status.HTTP_200_OK)
