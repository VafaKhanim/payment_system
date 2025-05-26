from cryptography.fernet import Fernet

def generate_fernet_key():
    key = Fernet.generate_key()
    print("Aşağıdakı açarı .env faylınıza əlavə edin:")
    print(f"FERNET_SECRET_KEY={key.decode()}")

if __name__ == "__main__":
    generate_fernet_key()