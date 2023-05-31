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
    name, phone_no = get_body_contents(event)

    query_select_user_by_name = '''
        SELECT *
        FROM "user"
            WHERE "user".name = %s
    '''

    user = list(pg_util.execute_query(query_select_user_by_name, (name,)))

    is_not_exist_user = len(user) == 0

    if is_not_exist_user:
        query_insert_new_user = '''
                    INSERT INTO "user"(name, "phoneNo")
                    VALUES (%s, %s)
                    RETURNING *
                '''

        insert_query_result = pg_util.execute_and_returning_query(
            query_insert_new_user,
            (name, phone_no))
        user = list(insert_query_result)

    user = user[0]

    if user.get('phoneNo') != phone_no:
        update_query = f'''
            UPDATE "user"
            SET "phoneNo"='{phone_no}'
            WHERE "user"."name" = %s
            RETURNING *
        '''

        user = list(pg_util.execute_and_returning_query(
            update_query, 
            (name,))
        )[0]
        
    token = generate_jwt_token(user['id'], user['name'])
    
    return {
        'token': token,
        'name': user['name']
    }


def get_body_contents(event) -> tuple[str, str]:
    body_dict = Json.to_dict(event['body'])

    if 'name' not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, '아이디가 없습니다')
    if 'phoneNo' not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, '휴대폰 번호가 없습니다')

    return body_dict['name'], body_dict['phoneNo']
