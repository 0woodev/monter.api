import json
import logging

from common.Json import Json
from common.const import ConstAWS, ConstHttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


def lambda_handler(event, context):

    return {
        "headers": {
            "Location": "https://naver.com"
        },
        "body": Json.to_json_string({}),
        ConstHttp.STATUS_CODE: 302
    }
