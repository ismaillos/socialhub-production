
from cryptography.fernet import Fernet
from config import settings

fernet = Fernet(settings.encryption_key.encode())

def encrypt_value(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt_value(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()
