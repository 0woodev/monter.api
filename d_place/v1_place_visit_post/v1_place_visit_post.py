import datetime
import logging

from common.CommonResultCode import CommonResultCode
from common.Json import Json
from common.MonterException import MonterException
from common.authorizer import authorizer, get_requester_id
from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
@authorizer
def lambda_handler(event, context):
    place_id, solved_log, visited_at = get_body_contents(event)
    user_id = get_requester_id(event)

    query = f'''
        INSERT INTO place_to_user("userId", "placeId", "solvedLog", "visitedAt")
        VALUES (%s, %s, %s, %s)
    '''

    pg_util.insert_query(query, (user_id, place_id, solved_log, visited_at))

    return


def get_body_contents(event):
    body_dict = Json.to_dict(event['body'])

    if "placeId" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "placeId 가 없습니다")
    if "solvedLog" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "solvedLog 가 없습니다")
    if "visitedAt" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "visitedAt 가 없습니다")

    return body_dict["placeId"], body_dict["solvedLog"], body_dict["visitedAt"]


