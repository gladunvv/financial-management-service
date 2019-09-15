from rest_framework import serializers
from django.contrib.auth.models import User

from wallet.models import Wallet, Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'type_trans', 'date_time', 'comment')

    def create(self, validate_data):
        wallet = validate_data['wallet']
        amount = validate_data['amount']
        type_trans = validate_data['type_trans']
        comment = validate_data['comment']
        trans = Transaction(
            wallet=wallet,
            amount=amount,
            type_trans=type_trans,
            comment=comment
        )
        search_error = trans.save()
        try:
            search_error = search_error.get('error', None)
        except:
            return trans
        else:
            if search_error:
                raise serializers.ValidationError({'detail': search_error})

class WalletWithTransSerializer(serializers.ModelSerializer):

    transactions = TransactionSerializer(many=True)
    
    class Meta:
        model = Wallet
        fields = ('id', 'name', 'balance', 'transactions')



class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('id', 'name')
        read_only_fields = ('balance',)
