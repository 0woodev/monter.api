import base64
import logging

import jwt
from cryptography.fernet import Fernet

from common.CommonResultCode import CommonResultCode
from common.MonterException import MonterException
from common.const import JWT_BYTE_SECRET_KEY

fernet: Fernet = None
algorithm = "HS256"

logger = logging.getLogger("api.jwt_util")


def prepare_encrypt():
    global fernet

    try:
        private_key = JWT_BYTE_SECRET_KEY
        private_key_bytes = bytes(private_key)
        encrypt_key = base64.urlsafe_b64encode(private_key_bytes)

        fernet = Fernet(encrypt_key)
    except Exception as exc:
        logger.exception(exc)


def decode_jwt_token(token):
    try:
        private_key = JWT_BYTE_SECRET_KEY
        str_private_key = str(private_key, "UTF-8")
        payload = jwt.decode(jwt=token, key=str_private_key, algorithms=["HS256"])

        return payload
    except Exception as exc:
        raise MonterException(CommonResultCode.UNAUTHORIZED, exc, "jwt 디코딩에 실패했습니다")


def encrypt(data):
    return fernet.encrypt(bytes(data, "utf-8"))


def decrypt(data):
    return fernet.decrypt(data)
