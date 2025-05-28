from django.contrib import admin
from .models import Card, Payment


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['get_masked_number', 'balance', 'created_at']
    search_fields = ['card_holder']
    readonly_fields = ['created_at']

    def get_masked_number(self, obj):
        return obj.get_masked_number()

    get_masked_number.short_description = 'Card Number'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    readonly_fields = ['payment_id', 'created_at', 'updated_at']
