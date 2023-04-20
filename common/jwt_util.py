import base64
import logging
from datetime import datetime, timedelta

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
        encrypt_key = base64.urlsafe_b64encode(JWT_BYTE_SECRET_KEY)

        fernet = Fernet(encrypt_key)
    except Exception as exc:
        logger.exception(exc)


def generate_jwt_token(user_id, name):
    try:
        prepare_encrypt()

        issue_at = datetime.now() - timedelta(minutes=1)
        expire_at = issue_at + timedelta(days=30)

        payload = {
            # registered claim
            "iss": "tbd-alpha.vercel.app/",
            "iat": issue_at.timestamp(),
            "exp": expire_at.timestamp(),
            # private claim
            'id': user_id,
            'name': name
        }

        str_private_key = str(JWT_BYTE_SECRET_KEY, "UTF-8")
        token = jwt.encode(payload=payload, key=str_private_key, algorithm=algorithm)

        return token
    except Exception as exc:
        raise exc


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
