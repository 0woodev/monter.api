import logging

from common.const import ConstAWS
from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
def lambda_handler(event, context):
    name = event[ConstAWS.PATH_PARAMETERS].get("name")

    query_select_user_by_name = '''
        SELECT *
        FROM "user"
        WHERE "user"."name" = %s
    '''

    user = list(pg_util.execute_query(query_select_user_by_name, (name,)))

    is_duplicate_name = len(user) != 0

    return {
        'is_duplicate_name': is_duplicate_name,
    }
