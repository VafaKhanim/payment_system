from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Card(models.Model):
    user_id = models.IntegerField()
    encrypted_card_number = models.TextField()
    encrypted_expiry_date = models.TextField()
    encrypted_cvv = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card for user_id {self.user_id}"

class Payment(models.Model):
    user_id = models.IntegerField()
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    event_id = models.IntegerField()
    ticket_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Payment by user_id {self.user_id} for event {self.event_id}"

    def save(self, *args, **kwargs):
        if not self.pk:
            # Get event price from Event service
            event_price = self.get_event_price()
            self.total_price = event_price * Decimal(str(self.ticket_count))
        super().save(*args, **kwargs)

    def get_event_price(self):
        import requests
        from django.conf import settings
        from decimal import Decimal

        try:
            response = requests.get(
                f"{settings.EVENT_SERVICE_URL}/api/events/{self.event_id}/"
            )
            response.raise_for_status()
            event_data = response.json()
            return Decimal(str(event_data.get('price', '0')))
        except Exception as e:

            return Decimal('0')


class MockBank(models.Model):
    card_number = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)
    expiry = models.CharField(max_length=5)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"MockBank card {self.card_number}"


