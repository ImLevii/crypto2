from rest_framework import serializers

from apollo.api.models import StoreTransaction, StoreVariables


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return round(value.timestamp() * 1000)


class StoreTransactionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    tx_status = serializers.ReadOnlyField()
    currency = serializers.ReadOnlyField()
    exchange_rate = serializers.ReadOnlyField()
    crypto_amount = serializers.ReadOnlyField()
    receiving_address = serializers.ReadOnlyField()
    confirmations_needed = serializers.ReadOnlyField()
    received_at = serializers.ReadOnlyField()
    received_amount = serializers.ReadOnlyField()
    received_confirmations = serializers.ReadOnlyField()
    destination_tag = serializers.ReadOnlyField()
    qr_code_url = serializers.ReadOnlyField()
    created_at = TimestampField()
    expires_at = TimestampField()
    last_updated = TimestampField()
    gift_card = serializers.ReadOnlyField()

    class Meta:
        model = StoreTransaction
        fields = ['id', 'currency', 'exchange_rate', 'crypto_amount', 'receiving_address', 'confirmations_needed', 'received_at', 'received_amount', 'received_confirmations', 'destination_tag', 'qr_code_url', 'tx_status', 'created_at', 'expires_at', 'last_updated', 'gift_card']


class StoreVariablesSerializer(serializers.ModelSerializer):
    extra_credit_enabled = serializers.ReadOnlyField()
    extra_credit_percentage = serializers.ReadOnlyField()

    class Meta:
        model = StoreVariables
        fields = ['extra_credit_enabled', 'extra_credit_percentage']
