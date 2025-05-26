from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Card, Payment, MockBank
from .serializers import CardSerializer, PaymentSerializer
from .utils.encryption import decrypt_data
from .utils.verification import luhn_checksum
from decimal import Decimal
import requests
import uuid
from django.conf import settings
from rest_framework.exceptions import ValidationError



class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)



class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        payment = serializer.save(
            user_id=self.request.user.id,
            payment_reference=f"PAY-{uuid.uuid4().hex[:10].upper()}"
        )
        self.process_payment(payment)

    def process_payment(self, payment):
        try:
            if payment.card is None:
                raise ValueError("Payment must be associated with a card")
            card = payment.card
            decrypted_card_number = decrypt_data(card.encrypted_card_number)
            decrypted_cvv = decrypt_data(card.encrypted_cvv)
            decrypted_expiry = decrypt_data(card.encrypted_expiry_date)


            mock_card = MockBank.objects.filter(
                card_number=decrypted_card_number,
                cvv=decrypted_cvv,
                expiry=decrypted_expiry
            ).first()

            if not mock_card or mock_card.balance < payment.total_price:
                payment.is_successful = False
                payment.save()
                return


            mock_card.balance -= payment.total_price
            mock_card.save()


            payment.is_successful = True
            payment.save()


            self.notify_event_service(payment)

        except Exception as e:
            payment.is_successful = False
            payment.save()
            raise

    def notify_event_service(self, payment):
        ticket_data = {
            "event_id": payment.event_id,
            "user_id": payment.user_id,
            "ticket_count": payment.ticket_count,
            "payment_reference": payment.payment_reference
        }


        update_data = {
            "event_id": payment.event_id,
            "tickets_sold": payment.ticket_count,
            "total_earnings": str(payment.total_price)
        }

        try:
            requests.post(
                f"{settings.EVENT_SERVICE_URL}/api/my-tickets/",
                json=ticket_data,
                headers={"Content-Type": "application/json"}
            )


            requests.patch(
                f"{settings.EVENT_SERVICE_URL}/api/events/{payment.event_id}/update-sales/",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )

        except requests.exceptions.RequestException as e:
            pass


