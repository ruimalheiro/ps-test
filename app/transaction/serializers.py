from rest_framework import serializers
from base.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'date',
            'expense_type',
            'account_id',
            'amount',
            'is_deleted'
        )
        read_only_fields = ('id',)


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'date', 'expense_type', 'account_id', 'amount')
        read_only_fields = ('id',)
        extra_kwargs = {
            'date': {'write_only': True},
            'expense_type': {'write_only': True},
            'account_id': {'write_only': True},
            'amount': {'write_only': True},
        }
