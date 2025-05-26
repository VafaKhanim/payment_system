from rest_framework import serializers
from .models import Card, Payment
from .utils.encryption import encrypt_data
from .utils.verification import luhn_checksum  # bu faylı aşağıda izah edəcəm

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'user_id', 'card_number', 'expiry_date', 'cvv']
        extra_kwargs = {
            'user_id': {'read_only': True}
        }

    card_number = serializers.CharField(write_only=True)
    expiry_date = serializers.CharField(write_only=True)
    cvv = serializers.CharField(write_only=True)

    def validate_card_number(self, value):
        if not luhn_checksum(value):
            raise serializers.ValidationError("Invalid card number (failed Luhn check).")
        return value

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        encrypted_card_number = encrypt_data(validated_data['card_number'])
        encrypted_expiry_date = encrypt_data(validated_data['expiry_date'])
        encrypted_cvv = encrypt_data(validated_data['cvv'])

        return Card.objects.create(
            user_id=user_id,
            encrypted_card_number=encrypted_card_number,
            encrypted_expiry_date=encrypted_expiry_date,
            encrypted_cvv=encrypted_cvv
        )



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'card', 'event_id', 'ticket_count', 'total_price', 'created_at', 'is_successful']
        read_only_fields = ['total_price', 'created_at', 'is_successful']

    def validate(self, data):
        if data['ticket_count'] < 1:
            raise serializers.ValidationError("Ticket count must be at least 1.")
        return data