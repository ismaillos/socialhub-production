import os
from cryptography.fernet import Fernet
MASTER_ENV='SECRET_BOX_KEY'
MASTER_FILE=os.getenv('SECRET_BOX_KEY_FILE','secrets/master.key')
def _load_master_key()->bytes:
    k=os.getenv(MASTER_ENV)
    if k: return k.encode()
    if os.path.exists(MASTER_FILE):
        with open(MASTER_FILE,'rb') as f: return f.read().strip()
    raise RuntimeError('Set SECRET_BOX_KEY env or provide secrets/master.key')
def _fernet(): return Fernet(_load_master_key())
def encrypt_value(v:str)->str: return _fernet().encrypt(v.encode()).decode()
def decrypt_value(v:str)->str: return _fernet().decrypt(v.encode()).decode()
