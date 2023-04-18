import logging

from common.CommonResultCode import CommonResultCode
from common.Json import Json
from common.MonterException import MonterException
from common.authorizer import get_requester_id, authorizer
from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
@authorizer
def lambda_handler(event, context):
    user_id = get_requester_id(event)
    visit_log_id = event['pathParameters'].get("id")

    body = get_body_contents(event)
    update_attributes = list(body.keys())
    update_values_tuple = tuple(map(lambda attr: body[attr], update_attributes))

    update_data_str = ', '.join(map(lambda attr: f'"{attr}" = %s', update_attributes))
    update_query = f'''
        UPDATE "place_to_user"
        SET {update_data_str}
        WHERE "place_to_user".id = %s
            AND "place_to_user"."isDeleted" = false
        RETURNING *
    '''

    update_query_response = list(
        pg_util.execute_and_returning_query(update_query, (*update_values_tuple, visit_log_id))
    )

    if len(update_query_response) == 0:
        raise MonterException(CommonResultCode.RESOURCE_NOT_FOUND, None, "해당하는 방문기록이 없습니다")
    else:
        return update_query_response[0]


def get_body_contents(event) -> dict:
    body_dict = Json.to_dict(event['body'])

    if "placeId" in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "방문 장소(placeId)는 수정할 수 없습니다")
    if "userId" in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "userId 는 수정할 수 없습니다")
    if "id" in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "id 는 수정할 수 없습니다")
    if "createdAt" in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "생성 시간(createdAt)는 수정할 수 없습니다")
    if "updatedAt" in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "수정 시간(updatedAt)는 수정할 수 없습니다")


    return body_dict
