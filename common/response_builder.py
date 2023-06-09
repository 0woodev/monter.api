import logging
import traceback
from http import HTTPStatus

from common.CommonResultCode import CommonResultCode
from common.Json import Json
from common.MonterException import MonterException
from common.const import ConstHttp, MonterResponseBody

logger = logging.getLogger('api.response_builder')


def init_json_response():
    default_attrs = {
        ConstHttp.HEADERS: {
            ConstHttp.CONTENT_TYPE: ConstHttp.APPLICATION_JSON,
            # ConstHttp.ACCESS_CONTROL_ALLOW_ORIGIN: '*',
            # ConstHttp.ACCESS_CONTROL_ALLOW_METHODS: 'GET,POST,PUT,DELETE',
            # ConstHttp.ACCESS_CONTROL_ALLOW_HEADERS: 'Authorization,Content-Type',
            # ConstHttp.ACCESS_CONTROL_MAX_AGE: 86400
        },
        ConstHttp.IS_BASE_64_ENCODED: False,
    }

    return {
        ConstHttp.STATUS_CODE: HTTPStatus.INTERNAL_SERVER_ERROR,
        ConstHttp.BODY: str(None),
        **default_attrs
    }


def build_response(response_object):
    try:
        response = init_json_response()

        monter_response_body = {
            MonterResponseBody.STATUS_CODE: HTTPStatus.OK,
            MonterResponseBody.MESSAGE: 'success'
        }
        if response_object is not None:
            monter_response_body['data'] = response_object

        response[ConstHttp.BODY] = Json.to_json_string(monter_response_body)
        response[ConstHttp.STATUS_CODE] = HTTPStatus.OK
        return response
    except Exception as exc:
        return __get_response_for_fail_in_building_response(exc)


def build_fail_response(err):
    try:
        response = init_json_response()

        if isinstance(err, MonterException):
            result_code = err.result_code

            monter_response_body = {
                'statusCode': result_code.status_code,
                'message': err.data,
                'error': result_code.status_code_string if err.exception is None else err.exception.__class__
            }
            response[ConstHttp.STATUS_CODE] = result_code.status_code
            response[ConstHttp.BODY] = Json.to_json_string(monter_response_body)
        else:  # UNHANDLED_ERROR
            logger.error(traceback.format_exc())

            result_code = CommonResultCode.MONTER_UNEXPECTED_ERROR

            monter_response_body = {
                'statusCode': result_code.status_code,
                'message': result_code.message,
                'error': {
                    "name": err.__class__.__name__,
                    "cause": err.__str__()
                }
            }

            response[ConstHttp.STATUS_CODE] = result_code.status_code
            response[ConstHttp.BODY] = Json.to_json_string(monter_response_body)
        return response
    except Exception as exc:
        return __get_response_for_fail_in_building_response(exc)


def __get_response_for_fail_in_building_response(err):

    response = init_json_response()
    response[ConstHttp.BODY] = Json.to_json_string({
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'error': 'Build Response Fail',
            'message': f'응답값에 이상이 있습니다.',
        })

    return response
