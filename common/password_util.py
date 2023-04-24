import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from common.const import ENCRYPT_KEY

fernet = None


def get_encrypt_key():
    key = ENCRYPT_KEY
    if key is None:
        return Fernet.generate_key()

    else:
        key_bytes = bytes(key, 'utf-8')
        return key_bytes



def get_fernet():
    global fernet

    if fernet is None:
        fernet = Fernet(get_encrypt_key())

    return fernet


def generate_salt() -> bytes:
    return base64.urlsafe_b64encode(os.urandom(16))


def hash_password(salt, password) -> bytes:
    encoded_password = password.encode()
    print(f"after_encoding: {encoded_password}")
    salted_password = salt + encoded_password
    print(f"after_salt: {salted_password}")
    f = get_fernet()
    hashed_password = f.encrypt(salted_password)
    print(f"after_hash: {hashed_password}")
    return hashed_password


def verify_password(user, password_from_client) -> bool:
    user_salt_str_from_db = user.get('salt')
    user_salt_bytes_from_db = bytes(user_salt_str_from_db, 'utf-8')

    encrypted_password_str_from_db = user.get('password')
    encrypted_password_bytes_from_db = bytes(encrypted_password_str_from_db, 'utf-8')

    encrypted_password_bytes_from_client = hash_password(user_salt_bytes_from_db, password_from_client)
    print(f"client 로 부터 받은 값: {encrypted_password_bytes_from_client}")
    return encrypted_password_bytes_from_db == encrypted_password_bytes_from_client
