import logging

import requests

from common.CommonResultCode import CommonResultCode
from common.MonterException import MonterException
from common.authorizer import get_requester_id, authorizer, get_requester_name
from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
@authorizer
def lambda_handler(event, context):
    user_id = get_requester_id(event)
    user_name = get_requester_name(event)

    # scraping
    try:
        is_verified = check_insta_external_link(user_name)
    except Exception as exc:
        raise MonterException(CommonResultCode.INVALID_USER_NAME, exc, f'{user_name} 닉네임에 해당하는 인스타아이디가 동일하지 않습니다')

    update_query = f'''
        UPDATE "user"
        SET verified = %s
        WHERE "user".id = %s
        RETURNING id, name, verified
    '''

    update_query_response = list(
        pg_util.execute_and_returning_query(update_query, (is_verified, user_id))
    )

    if len(update_query_response) == 0:
        raise MonterException(CommonResultCode.RESOURCE_NOT_FOUND, None, "해당하는 유저가 없습니다")
    else:
        return update_query_response[0]


def check_insta_external_link(user_name):
    user_instagram_webpage = requests.get(f'https://instagram.com/{user_name}/')
    at_sign = "\\u0040"
    is_verified = str(user_instagram_webpage.content, 'utf-8').find(f'monter.fun\/{at_sign}{user_name}') != -1
    return is_verified
