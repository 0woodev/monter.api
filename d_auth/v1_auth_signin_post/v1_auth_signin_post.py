import logging

from common.CommonResultCode import CommonResultCode
from common.Json import Json
from common.MonterException import MonterException
from common.jwt_util import generate_jwt_token
from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
def lambda_handler(event, context):
    name, password = get_body_contents(event)

    query_select_user_by_name = '''
        SELECT *
        FROM "user"
        WHERE "user"."name" = %s
            AND "user".password = %s
    '''

    user = list(pg_util.execute_query(query_select_user_by_name, (name, password)))

    is_exist_user = len(user) != 0
    if not is_exist_user:
        raise MonterException(CommonResultCode.RESOURCE_ALREADY_EXIST, None, "해당하는")

    user = list(user)[0]
    token = generate_jwt_token(user["id"], user['name'])

    return {
        'token': token,
        'name': user['name']
    }


def get_body_contents(event) -> tuple[str, str]:
    body_dict = Json.to_dict(event['body'])

    if "name" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "아이디가 없습니다")
    if "password" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "비밀번호가 없습니다")

    return body_dict['name'], body_dict['password']
