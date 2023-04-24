import logging
from http import HTTPStatus

from common.const import ConstAWS, ConstHttp
from common.pg_util import pg_util
from common.response_builder import build_fail_response, init_json_response, build_response
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

    return is_duplicate_name

