import logging

from common.CommonResultCode import CommonResultCode
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
    visit_log_id = event['pathParameters'].get("id")

    delete_query = f'''
        DELETE FROM place_to_user
        WHERE place_to_user."id" = %s
            AND place_to_user."userId" = %s
            RETURNING *
    '''

    visit_logs = list(pg_util.execute_and_returning_query(delete_query, (visit_log_id, user_id)))

    if len(visit_logs) == 0:
        raise MonterException(CommonResultCode.RESOURCE_NOT_FOUND, None, "해당하는 방문기록이 없습니다")
    else:
        return visit_logs[0]
