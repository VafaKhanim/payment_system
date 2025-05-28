from django.core.management.base import BaseCommand
from payment_app.models import Card



class Command(BaseCommand):
    help = 'Create test cards for mock bank database'

    def handle(self, *args, **options):
        test_cards_data = [
            {
                'card_number': '4111111111111111',  # Valid Visa test number
                'card_holder': 'John Doe',
                'expiry_date': '12/26',
                'cvv': '123',
                'balance': 1000.00
            }
        ]

        for card_data in test_cards_data:
            card = Card(balance=card_data['balance'])
            card._raw_data = {
                'card_number': card_data['card_number'],
                'card_holder': card_data['card_holder'],
                'expiry_date': card_data['expiry_date'],
                'cvv': card_data['cvv']
            }
            card.save()
            self.stdout.write(f"Created card: {card}")