from cryptography.fernet import Fernet
import base64
import os
from dotenv import load_dotenv

load_dotenv()


class CardEncryption:
    def __init__(self):
        env_key = os.getenv('FERNET_KEY')

        if env_key:
            self.key = env_key.encode()
        else:
            raise ValueError("FERNET_KEY is missing in environment variables (.env)")

        self.fernet = Fernet(self.key)

    def encrypt_card_data(self, card_data):
        try:
            encrypted_data = {}
            for field, value in card_data.items():
                if value:
                    encrypted_value = self.fernet.encrypt(str(value).encode())
                    encrypted_data[field] = base64.urlsafe_b64encode(encrypted_value).decode()
                else:
                    encrypted_data[field] = value
            return encrypted_data
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")

    def decrypt_card_data(self, encrypted_data):
        try:
            decrypted_data = {}
            for field, value in encrypted_data.items():
                if value and field in ['card_number', 'cvv', 'card_holder', 'expiry_date']:
                    encrypted_bytes = base64.urlsafe_b64decode(value.encode())
                    decrypted_value = self.fernet.decrypt(encrypted_bytes).decode()
                    decrypted_data[field] = decrypted_value
                else:
                    decrypted_data[field] = value
            return decrypted_data
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")