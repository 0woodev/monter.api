import logging

from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
def lambda_handler(event, context):
    select_target_user_query = f'''
            SELECT id, name, verified
            FROM "user"
        '''

    users = list(pg_util.execute_query(select_target_user_query))

    return users
