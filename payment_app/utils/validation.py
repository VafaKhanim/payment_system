import re
from datetime import datetime


class CardValidator:

    @staticmethod
    def luhn_check(card_number):
        """Luhn algoritmi ile card number-i validate edir"""

        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0

    @staticmethod
    def validate_card_number(card_number):
        """Card number-i validate edir"""
        if not card_number:
            return False, "Card number is required"

        # Yalniz reqemler
        if not re.match(r'^\d+$', card_number):
            return False, "Card number must contain only digits"

        # Uzunlugu 13-19 arasi olmalidir
        if len(card_number) < 13 or len(card_number) > 19:
            return False, "Card number must be between 13-19 digits"

        # Luhn check
        if not CardValidator.luhn_check(card_number):
            return False, "Invalid card number"

        return True, "Valid"

    @staticmethod
    def validate_expiry_date(expiry_date):
        """Expiry date-i validate edir (MM/YY format)"""
        if not expiry_date:
            return False, "Expiry date is required"

        if not re.match(r'^\d{2}/\d{2}$', expiry_date):
            return False, "Expiry date format must be MM/YY"

        try:
            month, year = expiry_date.split('/')
            month = int(month)
            year = 2000 + int(year)

            if month < 1 or month > 12:
                return False, "Invalid month"

            # Keçmiş tarixi yoxla
            current_date = datetime.now()
            card_date = datetime(year, month, 1)

            if card_date < current_date.replace(day=1):
                return False, "Card has expired"

            return True, "Valid"

        except ValueError:
            return False, "Invalid expiry date"

    @staticmethod
    def validate_cvv(cvv):
        """CVV-i validate edir"""
        if not cvv:
            return False, "CVV is required"

        if not re.match(r'^\d{3,4}$', cvv):
            return False, "CVV must be 3 or 4 digits"

        return True, "Valid"

    @staticmethod
    def validate_card_holder(card_holder):
        """Card holder name-i validate edir"""
        if not card_holder:
            return False, "Card holder name is required"

        if len(card_holder.strip()) < 2:
            return False, "Card holder name must be at least 2 characters"

        # Yalniz herf ve boşluq
        if not re.match(r'^[a-zA-Z\s]+$', card_holder.strip()):
            return False, "Card holder name must contain only letters and spaces"

        return True, "Valid"

    @staticmethod
    def validate_card_data(card_data):
        """Bütün card məlumatlarını validate edir"""
        errors = {}

        # Card number
        is_valid, message = CardValidator.validate_card_number(card_data.get('card_number'))
        if not is_valid:
            errors['card_number'] = message

        # Card holder
        is_valid, message = CardValidator.validate_card_holder(card_data.get('card_holder'))
        if not is_valid:
            errors['card_holder'] = message

        # Expiry date
        is_valid, message = CardValidator.validate_expiry_date(card_data.get('expiry_date'))
        if not is_valid:
            errors['expiry_date'] = message

        # CVV
        is_valid, message = CardValidator.validate_cvv(card_data.get('cvv'))
        if not is_valid:
            errors['cvv'] = message

        return len(errors) == 0, errors


