from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from wallet.models import Wallet, Transaction

from wallet.serializers import (
    WalletWithTransSerializer,
    WalletSerializer,
    TransactionSerializer,
    )


class OneWalletView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk)
        serializer = WalletWithTransSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk)
        data = request.data
        serializer = WalletSerializer(wallet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk)
        wallet.delete()
        msg = {
            'message': 'Your wallet has been successfully deleted'
        }
        return Response(msg, status=status.HTTP_200_OK)


class CreateWalletView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data
        user = request.user
        serializer = WalletSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllWalletView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllTransactionView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTransactionView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, requset):
        data = requset.data
        wallet = get_object_or_404(Wallet, pk=requset.data['wallet'])

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(wallet=wallet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTransactionView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.delete()
        msg = {
            'message': 'Your transaction was successfully deleted'
        }
        return Response(msg, status=status.HTTP_200_OK)
