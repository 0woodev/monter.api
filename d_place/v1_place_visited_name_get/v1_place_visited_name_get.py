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
    select_target_user_query = f'''
        SELECT id, name
        FROM "user"
        WHERE "user".name = %s
    '''

    user = list(pg_util.execute_query(select_target_user_query, (name,)))
    if len(user) == 0:
        raise MonterException(CommonResultCode.RESOURCE_NOT_FOUND, None, "유저가 존재하지 않습니다")
    else:
        user = user[0]

    select_target_user_query = f'''
        SELECT id, "userId", "placeId", "solvedLog", "createdAt", "updatedAt", "visitedAt", "colorHex"
        FROM place_to_user
        WHERE place_to_user."userId" = %s
    '''
    visit_logs = pg_util.execute_query(select_target_user_query, (user.get("id"),))

    return list(visit_logs)
