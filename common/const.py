import os
import logging

logger = logging.getLogger("api.const")

JWT_COOKIE_KEY_NAME = "B48Gd6N0uMbHTU/WFNwhSkrApkUoDYaVkSQhALAowqfEzAo6fMXmKT927J+i8H7U7f/GfZABDUiG sOL/oydusQ=="
JWT_BYTE_SECRET_KEY: bytes = b"B48Gd6N0uMbHTU/WFNwhSkrApkUoDYaVkSQhALAowqfEzAo6fMXmKT927J+i8H7U7f/GfZABDUiG sOL/oydusQ=="
# JWT_BYTE_SECRET_KEY: bytes = b"FuybjQzruy580KNnfS6DYzINSIBU8hd1"


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
    PLAIN_TEXT = "plain/text"
    HEADERS = "headers"
    CONTENT_TYPE = "Content-Type"
    STATUS_CODE = "statusCode"
    IS_BASE_64_ENCODED = "isBase64Encoded"
    APPLICATION_JSON = "application/json"
    BODY = "body"

