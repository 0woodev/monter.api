import logging

from common.CommonResultCode import CommonResultCode
from common.MonterException import MonterException
from common.const import ConstAWS
from common.jwt_util import decode_jwt_token

logger = logging.getLogger("api.authorizer")


def authorizer(func):
    def wrapper(*args, **kwargs):
        event = args[0]
        context = args[1]

        try:
            token = _validate_and_extract_input_for_token(event)
            data = decode_jwt_token(token=token)

            event['requestContext'] = {
                'authorizer': {'id': data["id"], 'name': data["name"]}
            }

            return func(event, context)
        except MonterException as exc:
            raise exc
        except Exception as exc:
            raise exc

    return wrapper


def _validate_and_extract_input_for_token(event):
    if 'headers' not in event:
        raise MonterException(CommonResultCode.INVALID_HEADERS, None, data='headers 가 없습니다')

    event['headers'] = _lowercase_dict_key(event['headers'])

    authorization = event['headers'].get(ConstAWS.AUTHORIZATION)
    if authorization is None or not authorization.startswith('Bearer '):
        raise MonterException(CommonResultCode.UNAUTHORIZED, None, data='Authorization: Bearer token is invalid')

    token = authorization[7:]
    return token


def _lowercase_dict_key(data: dict) -> dict:
    result = dict()

    for key, value in data.items():
        if isinstance(value, dict):
            result[key.lower()] = _lowercase_dict_key(value)
        else:
            result[key.lower()] = value

    return result


def get_requester_id(event):
    if 'requestContext' not in event:
        raise MonterException(CommonResultCode.INTERNAL_SERVICE_ERROR, None, 'event 의 requestContext 가 없습니다')

    if 'authorizer' not in event['requestContext']:
        raise MonterException(CommonResultCode.INTERNAL_SERVICE_ERROR, None, 'requestContext 의 authorizer 가 없습니다')

    if 'id' not in event['requestContext']['authorizer']:
        raise MonterException(CommonResultCode.INTERNAL_SERVICE_ERROR, None, 'authorizer 에 id 가 없습니다')

    return event['requestContext']['authorizer']['id']


def get_requester_name(event):
    if 'requestContext' not in event:
        raise MonterException(CommonResultCode.INTERNAL_SERVICE_ERROR, None, 'event 의 requestContext 가 없습니다')

    if 'authorizer' not in event['requestContext']:
        raise MonterException(CommonResultCode.INTERNAL_SERVICE_ERROR, None, 'requestContext 의 authorizer 가 없습니다')

    if 'name' not in event['requestContext']['authorizer']:
        raise MonterException(CommonResultCode.INTERNAL_SERVICE_ERROR, None, 'authorizer 에 id 가 없습니다')

    return event['requestContext']['authorizer']['name']
