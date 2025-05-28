from rest_framework import serializers
from .models import Payment, Card
from .utils.validation import CardValidator
from decimal import Decimal


class PaymentCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    callback_url = serializers.URLField()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value


class CardDataSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=19, min_length=13)
    card_holder = serializers.CharField(max_length=100, min_length=2)
    expiry_date = serializers.CharField(max_length=5)
    cvv = serializers.CharField(max_length=4, min_length=3)

    def validate(self, data):
        # Card validation
        is_valid, errors = CardValidator.validate_card_data(data)
        if not is_valid:
            raise serializers.ValidationError(errors)
        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_id', 'amount', 'status', 'created_at']