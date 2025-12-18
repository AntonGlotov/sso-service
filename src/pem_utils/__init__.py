from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from config import settings


def get_private_key():
    with open(settings.pem_path_private, "rb") as key_file:
        return load_pem_private_key(key_file.read(), password=settings.PASSPHRASE.encode())

def get_public_key():
    with open(settings.pem_path_public, "rb") as key_file:
        return load_pem_public_key(key_file.read())