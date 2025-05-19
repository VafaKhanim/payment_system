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
