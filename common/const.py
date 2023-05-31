import os
import logging

logger = logging.getLogger("api.const")


def get_os_or_file(env_name, filename):
    env = os.environ.get(env_name, 'not-assigned')

    if env == 'not-assigned':
        file = os.path.join(os.path.dirname(__file__), f"../../env/{filename}.txt")
        file = os.path.abspath(file)
        f = open(file, "r")
        env = f.read().strip().strip("\"")
        f.close()

    return env


# 64 encoded 32 bytes key
JWT_SECRET_KEY = os.environ.get('jwt_secret_key', "not-assigned")
try:
    if JWT_SECRET_KEY == 'not-assigned':
        jwt_secret_key_file_name = os.path.join(os.path.dirname(__file__), "../../env/jwt_secret_key.txt")
        jwt_secret_key_file_name = os.path.abspath(jwt_secret_key_file_name)
        f = open(jwt_secret_key_file_name, "r")
        JWT_SECRET_KEY = f.read().strip().strip("\"")
        f.close()
except:
    logger.exception("read jwt secret key error")
JWT_BYTE_SECRET_KEY: bytes = bytes(JWT_SECRET_KEY, 'utf-8')

ENCRYPT_KEY = os.environ.get('encrypt_key', 'not-assigned')


class Postgres:
    ENDPOINT = os.environ.get('postgres_endpoint', 'not-assigned')
    SCHEMA_NAME = os.environ.get('postgres_db_name', 'not-assigned')
    USER = os.environ.get('postgres_db_user', 'not-assigned')
    PASSWORD = os.environ.get('postgres_db_password', 'not-assigned')

    try:
        if ENDPOINT == "not-assigned":
            file_db_endpoint = os.path.join(os.path.dirname(__file__), "../../env/db_endpoint.txt")
            file_db_endpoint = os.path.abspath(file_db_endpoint)
            f = open(file_db_endpoint, "r")
            ENDPOINT = f.read().strip().strip("\"")
            f.close()
            file_db_name = os.path.join(os.path.dirname(__file__), "../../env/db_name.txt")
            file_db_name = os.path.abspath(file_db_name)
            f = open(file_db_name, "r")
            SCHEMA_NAME = f.read().strip().strip("\"")
            f.close()
            file_db_user = os.path.join(os.path.dirname(__file__), "../../env/db_user.txt")
            file_db_user = os.path.abspath(file_db_user)
            f = open(file_db_user, "r")
            USER = f.read().strip().strip("\"")
            f.close()
            file_db_password = os.path.join(os.path.dirname(__file__), "../../env/db_password_for_python.txt")
            file_db_password = os.path.abspath(file_db_password)
            f = open(file_db_password, "r")
            PASSWORD = f.read().strip().strip("\"")
            f.close()
    except Exception as err:
        logger.error("fail to load environments variable")


class ConstAWS:
    AUTHORIZER = "authorizer"
    AUTHORIZATION = "authorization"
    SESSION_OWNER_ID = "session_owner_id"
    HEADER = "headers"
    MULTI_VALUE_HEADER = "multiValueHeaders"
    QUERY_PARAMETER = "queryStringParameters"
    PATH_PARAMETERS = "pathParameters"
    REQUEST_CONTEXT = "requestContext"
    BODY_CONTENTS = "body"
    STAGE_VARIABLES = "stageVariables"
    MESSAGE_ATTRIBUTES = "messageAttributes"


class ConstAlarm:
    ALARM_TOPIC_CONFIG = "topic"
    ALARM_TOPIC_DEVICE_STATUS = "topic_status"


class ConstHttp:
    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
    ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
    ACCESS_CONTROL_MAX_AGE = "Access-Control-Max-Age"
    AUTHORIZATION = "Authorization"
    PLAIN_TEXT = "plain/text"
    HEADERS = "headers"
    CONTENT_TYPE = "Content-Type"
    STATUS_CODE = "statusCode"
    IS_BASE_64_ENCODED = "isBase64Encoded"
    APPLICATION_JSON = "application/json"
    BODY = "body"


class ConstTwilio:
    ACCOUNT_SID = get_os_or_file('account_sid', 'account_sid')
    AUTH_TOKEN = get_os_or_file('auth_token', 'auth_token')
    FROM = get_os_or_file('from', 'from')

    MESSAGE_FORMAT = '[monter climber] 인증번호 {code}'


class MonterResponseBody:
    STATUS_CODE = "statusCode"
    MESSAGE = "message"
    DATA = "data"


GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

NEW_USER_NAME_PREFIX = '__FIX_REQUIRED_MONTER__'
