import logging

import requests

from common.CommonResultCode import CommonResultCode
from common.Json import Json
from common.MonterException import MonterException
from common.const import ConstAWS, GOOGLE_USERINFO_URL
from common.jwt_util import generate_jwt_token
from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
def lambda_handler(event, context):
    token = event[ConstAWS.PATH_PARAMETERS].get("token")

    google_info = get_google_info(token)

    name = google_info.get('name')
    picture = google_info.get('picture')
    email = google_info.get('email')
    google_id = google_info.get('id')

    query_select_user_by_google_id = '''
        SELECT *
        FROM "user"
        WHERE "user"."googleId" = %s
    '''

    user = list(pg_util.get_select_query_result(query_select_user_by_google_id, (google_id,)))

    if len(user) == 0:
        query_insert_new_user = '''
            INSERT INTO "user"(name, picture, email, "googleId")
            VALUES (%s, %s, %s, %s)
            RETURNING *
        '''

        insert_query_result = pg_util.insert_and_returning_query(query_insert_new_user, (name, picture, email, google_id))

        user = list(insert_query_result)

    user = user[0]
    token = generate_jwt_token(user["id"], user['name'])

    return {
        'token': token,
        'name': user['name']
    }


def get_google_info(token):
    query_params = {'access_token': token}
    response = requests.get(f"{GOOGLE_USERINFO_URL}?access_token={query_params['access_token']}")

    if not response.ok:
        raise MonterException(CommonResultCode.UNAUTHORIZED, None, 'access token 이 올바르지 않습니다')

    user_info = Json.to_dict(response.content)

    if 'id' not in user_info:
        raise MonterException(CommonResultCode.UNAUTHORIZED, None, '구글로그인에 문제가 있습니다 ')

    logger.info(user_info)

    return user_info
