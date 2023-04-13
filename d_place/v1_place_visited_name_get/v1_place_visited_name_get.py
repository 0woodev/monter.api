import logging

from common.CommonResultCode import CommonResultCode
from common.MonterException import MonterException
from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
def lambda_handler(event, context):
    logger.warning(event)
    name = event['pathParameters'].get("name")
    query = f'''
        SELECT id, name
        FROM "user"
        WHERE "user".name = %s
    '''

    user = list(pg_util.get_select_query_result(query, (name, )))
    if len(user) == 0:
        raise MonterException(CommonResultCode.RESOURCE_NOT_FOUND, None, "유저가 존재하지 않습니다")
    else:
        user = user[0]

    query = f'''
        SELECT id, "userId", "placeId", "solvedLog", "createdAt", "updatedAt"
        FROM place_to_user
        WHERE place_to_user."userId" = %s
    '''
    visit_logs = pg_util.get_select_query_result(query, (user.get("id"), ))

    return list(visit_logs)
