from django.db import models
from django.conf import settings

class Card(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    encrypted_card_number = models.TextField()
    encrypted_expiry_date = models.TextField()
    encrypted_cvv = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card for {self.user}"

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    event_id = models.IntegerField()
    ticket_count = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment by {self.user.username} for event {self.event_id}"


class MockBank(models.Model):
    card_number = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)
    expiry = models.CharField(max_length=5)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"MockBank card {self.card_number}"


