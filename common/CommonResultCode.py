from enum import Enum
from http import HTTPStatus

from common.ResultCode import ResultCode


class CommonResultCode(ResultCode, Enum):
    SUCCESS = (HTTPStatus.OK, "SUCCESS", "success")
    UNAUTHORIZED = (HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "request unauthorized")
    INVALID_PARAMETER = (HTTPStatus.BAD_REQUEST, "INVALID_PARAMETER", "invalid parameter")
    PARAMETER_NOT_FOUND = (HTTPStatus.BAD_REQUEST, "PARAMETER_NOT_FOUND", "parameter not found")
    QUERY_NOT_FOUND = (HTTPStatus.BAD_REQUEST, "QUERY_NOT_FOUND", "query parameter not found")
    INVALID_REQUEST_BODY = (HTTPStatus.BAD_REQUEST, "INVALID_REQUEST_BODY", "invalid requestBody")
    BAD_REQUEST = (HTTPStatus.BAD_REQUEST, "BAD_REQUEST", "input is wrong")
    UNEXPECTED_QUERY_PARAMETER = (HTTPStatus.BAD_REQUEST, "UNEXPECTED_QUERY_PARAMETER", "unexpected query parameter")
    RESOURCE_NOT_FOUND = (HTTPStatus.BAD_REQUEST, "RESOURCE_NOT_FOUND", "can't find the resource")
    RESOURCE_ALREADY_EXIST = (HTTPStatus.BAD_REQUEST, "RESOURCE_ALREADY_EXIST", "resource is already exist")

    HTTP_METHOD_NOT_FOUND = (HTTPStatus.BAD_REQUEST, "HTTP_METHOD_NOT_FOUND", "can't find the HTTP method")

    DB_CONNECTION_ERROR = (HTTPStatus.INTERNAL_SERVER_ERROR, "DB_CONNECTION_ERROR", "DB Connection 을 확인하세요")

    INTERNAL_SERVICE_ERROR = (HTTPStatus.BAD_REQUEST, "INTERNAL_SERVICE_ERROR", "internal service is error")
    INVALID_QUERY_PARAMETER = (HTTPStatus.BAD_REQUEST, "INVALID_QUERY_PARAMETER", "invalid query parameter")
    INVALID_PATH_PARAMETER = (HTTPStatus.BAD_REQUEST, "INVALID_PATH_PARAMETER", "invalid path parameter")
    INVALID_AUTH_PARAMETER = (HTTPStatus.BAD_REQUEST, "INVALID_AUTH_PARAMETER", "invalid auth parameter")
    INVALID_BODY_CONTENTS = (HTTPStatus.BAD_REQUEST, "INVALID_BODY_CONTENTS", "invalid body contents")

    INVALID_PARAMETER_FOR_BUILD_PARTITION_KEY = (HTTPStatus.BAD_REQUEST,
                                                 "INVALID_PARAMETER_FOR_BUILD_PARTITION_KEY", "")
    INVALID_PARAMETER_FOR_BUILD_SORT_KEY = (HTTPStatus.BAD_REQUEST, "INVALID_PARAMETER_FOR_BUILD_SORT_KEY", "")

    PERMISSION_DENIED = (HTTPStatus.BAD_REQUEST, "PERMISSION_DENIED", "request is denied by permission")
    SORTKEY_IS_NOT_ALLOWED = (HTTPStatus.BAD_REQUEST, "SORTKEY_IS_NOT_ALLOWED", "sortKey is not allowed")

    HAVE_NO_PERMISSION_TO_MODIFY = (HTTPStatus.BAD_REQUEST,
                                    "HAVE_NO_PERMISSION_TO_MODIFY", "you do not have permission to modify")

    BUILD_RESPONSE_FAIL = (HTTPStatus.BAD_REQUEST, "BUILD_RESPONSE_FAIL", "BUILD_RESPONSE_FAIL")

    MONTER_UNEXPECTED_ERROR = (HTTPStatus.BAD_REQUEST, "MONTER_UNEXPECTED_ERROR", "MONTER_UNEXPECTED_ERROR")

    REDIRECT_TO_LEGACY = (HTTPStatus.FOUND, "REDIRECT_TO_LEGACY", "redirect to legacy server")
