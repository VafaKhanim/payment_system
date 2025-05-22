from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Card, Payment, MockBank
from .serializers import CardSerializer
from .crypto_utils import decrypt
from .utils import luhn_check
from decimal import Decimal

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

