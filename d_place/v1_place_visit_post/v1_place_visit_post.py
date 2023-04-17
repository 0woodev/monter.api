import logging
from datetime import datetime

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
    user_id = get_requester_id(event)
    place_id, solved_log, visited_at, color_hex = get_body_contents(event)

    is_today_first_visit = check_user_visit_or_not_today(user_id, place_id, visited_at)
    if not is_today_first_visit:
        raise MonterException(CommonResultCode.RESOURCE_ALREADY_EXIST, None, '금일 해당 클라이밍장에 방문한 기록이 있습니다.')

    saved_log = add_new_visit_log(color_hex, place_id, solved_log, user_id, visited_at)
    return saved_log


def add_new_visit_log(color_hex, place_id, solved_log, user_id, visited_at):
    try:
        add_new_visit_log_query = '''
            INSERT INTO place_to_user("userId", "placeId", "solvedLog", "visitedAt", "colorHex")
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        '''
        add_new_log_query_response = list(pg_util.execute_and_returning_query(
            add_new_visit_log_query,
            (user_id, place_id, solved_log, visited_at, color_hex)
        ))

        if len(add_new_log_query_response) == 0:
            raise MonterException(CommonResultCode.MONTER_UNEXPECTED_ERROR, None, '방문기록 저장에 실패했습니다')

        return add_new_log_query_response[0]
    except MonterException as exc:
        raise MonterException(exc.result_code, exc, exc.data)
    except Exception as exc:
        raise MonterException(CommonResultCode.MONTER_UNEXPECTED_ERROR, exc, '방문기록에 문제가 발생했습니다')


def check_user_visit_or_not_today(user_id, place_id, visited_at):
    try:
        visited_date = datetime.strptime(visited_at, '%Y-%m-%d %H:%M:%S').date().isoformat()
        check_visit_or_not_query = '''
            SELECT COUNT(*) as cnt
            FROM place_to_user
            WHERE to_char("visitedAt", 'yyyy-mm-dd') = %s
                AND "userId" = %s
                AND "placeId" = %s
        '''

        check_visit_query_response = list(pg_util.execute_query(
            check_visit_or_not_query,
            (visited_date, user_id, place_id)
        ))

        if len(check_visit_query_response) == 0:
            raise MonterException(CommonResultCode.MONTER_UNEXPECTED_ERROR, None, '방문기록 조회에 실패했습니다')

        return check_visit_query_response[0].get('cnt') == 0
    except Exception as exc:
        raise MonterException(CommonResultCode.MONTER_UNEXPECTED_ERROR, exc, '유저의 중복방문 체크 시 에러 발생')


def get_body_contents(event):
    body_dict = Json.to_dict(event['body'])

    if "placeId" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "placeId 가 없습니다")
    if "solvedLog" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "solvedLog 가 없습니다")
    if "visitedAt" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "visitedAt 가 없습니다")
    if "colorHex" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "colorHex 가 없습니다")

    return body_dict["placeId"], body_dict["solvedLog"], body_dict["visitedAt"], body_dict["colorHex"]
