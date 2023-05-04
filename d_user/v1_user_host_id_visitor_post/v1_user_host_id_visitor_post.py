import logging

from common.CommonResultCode import CommonResultCode
from common.Json import Json
from common.MonterException import MonterException
from common.const import ConstAWS
from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
def lambda_handler(event, context):
    date, host_id, visitorName = get_request_input(event)

    try:
        add_new_visit_log_query = '''
            INSERT INTO visitor(date, "visitorName", "hostId")
            VALUES (%s, %s, %s)
            RETURNING *
        '''
        add_new_log_query_response = list(pg_util.execute_and_returning_query(
            add_new_visit_log_query,
            (date, visitorName, host_id)
        ))

        if len(add_new_log_query_response) == 0:
            raise MonterException(CommonResultCode.MONTER_UNEXPECTED_ERROR, None, '방문기록 저장에 실패했습니다')

        return add_new_log_query_response[0]
    except MonterException as exc:
        raise MonterException(exc.result_code, exc, exc.data)
    except Exception as exc:
        raise MonterException(CommonResultCode.MONTER_UNEXPECTED_ERROR, exc, '방문기록에 문제가 발생했습니다')


def get_request_input(event) -> tuple[str, int, any]:
    body_dict = Json.to_dict(event['body'])

    if "date" not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, "date 가 없습니다")

    path_params = event[ConstAWS.PATH_PARAMETERS]

    if "host_id" not in path_params:
        raise MonterException(CommonResultCode.INVALID_PATH_PARAMETER, None, "host_id 가 없습니다")

    return body_dict['date'], int(path_params['host_id']), body_dict.get('visitorName')
