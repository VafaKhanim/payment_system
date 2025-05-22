from django.contrib import admin
from .models import Card, Payment, MockBank

admin.site.register(Card)
admin.site.register(Payment)
admin.site.register(MockBank)
