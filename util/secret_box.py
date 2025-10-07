import os
from cryptography.fernet import Fernet
MASTER_ENV = 'SECRET_BOX_KEY'
MASTER_FILE = os.getenv('SECRET_BOX_KEY_FILE', 'secrets/master.key')
def _load_master_key() -> bytes:
    key = os.getenv(MASTER_ENV)
    if key: return key.encode()
    if os.path.exists(MASTER_FILE):
        with open(MASTER_FILE,'rb') as f: return f.read().strip()
    raise RuntimeError('Secret box master key not found. Set SECRET_BOX_KEY env or provide secrets/master.key')
def _fernet() -> Fernet: return Fernet(_load_master_key())
def encrypt_value(plaintext: str) -> str: return _fernet().encrypt(plaintext.encode()).decode()
def decrypt_value(ciphertext: str) -> str: return _fernet().decrypt(ciphertext.encode()).decode()
