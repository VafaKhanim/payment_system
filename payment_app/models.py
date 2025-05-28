from django.db import models
from django.utils import timezone
from .utils.encryption import CardEncryption
import uuid


class Card(models.Model):
    card_number = models.TextField()  # Encrypted
    card_holder = models.TextField()  # Encrypted
    expiry_date = models.TextField()  # Encrypted
    cvv = models.TextField()  # Encrypted
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Eger decrypt olunmus data varsa encrypt et
        if hasattr(self, '_raw_data'):
            encryption = CardEncryption()
            encrypted_data = encryption.encrypt_card_data(self._raw_data)
            self.card_number = encrypted_data['card_number']
            self.card_holder = encrypted_data['card_holder']
            self.expiry_date = encrypted_data['expiry_date']
            self.cvv = encrypted_data['cvv']
        super().save(*args, **kwargs)

    def get_decrypted_data(self):
        """Decrypt olunmus card melumatlarini qaytarir"""
        encryption = CardEncryption()
        encrypted_data = {
            'card_number': self.card_number,
            'card_holder': self.card_holder,
            'expiry_date': self.expiry_date,
            'cvv': self.cvv
        }
        return encryption.decrypt_card_data(encrypted_data)

    def get_masked_number(self):
        """Maskalənmış card number qaytarır"""
        try:
            decrypted_data = self.get_decrypted_data()
            card_number = decrypted_data['card_number']
            return f"**** **** **** {card_number[-4:]}"
        except:
            return "**** **** **** ****"

    def __str__(self):
        return self.get_masked_number()


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    callback_url = models.URLField()
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.amount}"

