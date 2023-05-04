import datetime
import logging

from common.CommonResultCode import CommonResultCode
from common.MonterException import MonterException
from common.const import ConstAWS
from common.pg_util import pg_util
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
def lambda_handler(event, context):
    date: str = event.get(ConstAWS.QUERY_PARAMETER, {}).get('date', datetime.date.today().strftime('%Y-%m-%d'))
    host_id: int = int(event[ConstAWS.PATH_PARAMETERS]['host_id'])

    count_visitors_in_specific_date = f'''
        SELECT count(*)
        FROM visitor
        WHERE "hostId" = %s
            AND date = %s
    '''

    day_visitors_count_query_result = list(pg_util.execute_query(count_visitors_in_specific_date, (host_id, date)))
    if len(day_visitors_count_query_result) == 0 or 'count' not in day_visitors_count_query_result[0]:
        raise MonterException(CommonResultCode.DB_QUERY_ERROR, None, 'count query error')

    day_visitors_count = day_visitors_count_query_result[0]['count']

    count_all_visitors = f'''
        SELECT count(*)
        FROM visitor
        WHERE "hostId" = %s
    '''

    total_visitors_count_query_result = list(pg_util.execute_query(count_all_visitors, (host_id,)))
    if len(total_visitors_count_query_result) == 0 or 'count' not in total_visitors_count_query_result[0]:
        raise MonterException(CommonResultCode.DB_QUERY_ERROR, None, 'count query error')

    total_visitors_count = total_visitors_count_query_result[0]['count']

    return {
        'day': day_visitors_count,
        'total': total_visitors_count
    }
