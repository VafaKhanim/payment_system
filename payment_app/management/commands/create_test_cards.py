from django.core.management.base import BaseCommand
from payment_app.models import Card



class Command(BaseCommand):
    help = 'Create test cards for mock bank database'

    def handle(self, *args, **options):
        test_cards_data = [
            {
                'card_number': '4532123456789012',  # Valid Visa test number
                'card_holder': 'John Doe',
                'expiry_date': '12/26',
                'cvv': '123',
                'balance': 1000.00
            },
            {
                'card_number': '5555555555554444',  # Valid MasterCard test number
                'card_holder': 'Jane Smith',
                'expiry_date': '05/27',
                'cvv': '456',
                'balance': 500.00
            },
            {
                'card_number': '378282246310005',  # Valid Amex test number
                'card_holder': 'Test User',
                'expiry_date': '08/25',
                'cvv': '7893',
                'balance': 2000.00
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