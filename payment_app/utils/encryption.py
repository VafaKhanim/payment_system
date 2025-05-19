from cryptography.fernet import Fernet
import os

# Real layihədə bu açarı settings.py faylından ENV dəyişəni kimi oxumaq daha təhlükəsizdir
key = os.getenv('FERNET_SECRET_KEY')  # və ya settings.FERNET_SECRET_KEY
fernet = Fernet(key)

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

