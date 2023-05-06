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
    query_params = event.get(ConstAWS.QUERY_PARAMETER)
    if query_params is None:
        query_params = {'date': datetime.date.today().strftime('%Y-%m-%d')}

    date: str = query_params.get('date')
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


{'version': '1.0', 'resource': '/user/{host_id}/visitor', 'path': '/api/user/75/visitor', 'httpMethod': 'GET',
 'headers': {'Content-Length': '0', 'Host': '5g7vyrifn4.execute-api.ap-northeast-2.amazonaws.com',
             'Postman-Token': '290150f7-7465-4a39-bf50-8546fbcb5c60', 'User-Agent': 'PostmanRuntime/7.32.2',
             'X-Amzn-Trace-Id': 'Root=1-6455b43c-5b69d81645ffedd32adab7ab', 'X-Forwarded-For': '119.196.225.193',
             'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https', 'accept': '*/*',
             'accept-encoding': 'gzip, deflate, br'},
 'multiValueHeaders': {'Content-Length': ['0'], 'Host': ['5g7vyrifn4.execute-api.ap-northeast-2.amazonaws.com'],
                       'Postman-Token': ['290150f7-7465-4a39-bf50-8546fbcb5c60'],
                       'User-Agent': ['PostmanRuntime/7.32.2'],
                       'X-Amzn-Trace-Id': ['Root=1-6455b43c-5b69d81645ffedd32adab7ab'],
                       'X-Forwarded-For': ['119.196.225.193'], 'X-Forwarded-Port': ['443'],
                       'X-Forwarded-Proto': ['https'], 'accept': ['*/*'], 'accept-encoding': ['gzip, deflate, br']},
 'queryStringParameters': None, 'multiValueQueryStringParameters': None,
 'requestContext': {'accountId': '308340476166', 'apiId': '5g7vyrifn4',
                    'domainName': '5g7vyrifn4.execute-api.ap-northeast-2.amazonaws.com', 'domainPrefix': '5g7vyrifn4',
                    'extendedRequestId': 'EekZhhO4IE0EPWA=', 'httpMethod': 'GET',
                    'identity': {'accessKey': None, 'accountId': None, 'caller': None, 'cognitoAmr': None,
                                 'cognitoAuthenticationProvider': None, 'cognitoAuthenticationType': None,
                                 'cognitoIdentityId': None, 'cognitoIdentityPoolId': None, 'principalOrgId': None,
                                 'sourceIp': '119.196.225.193', 'user': None, 'userAgent': 'PostmanRuntime/7.32.2',
                                 'userArn': None}, 'path': '/api/user/75/visitor', 'protocol': 'HTTP/1.1',
                    'requestId': 'EekZhhO4IE0EPWA=', 'requestTime': '06/May/2023:01:58:20 +0000',
                    'requestTimeEpoch': 1683338300660, 'resourceId': 'GET /user/{host_id}/visitor',
                    'resourcePath': '/user/{host_id}/visitor', 'stage': 'api'}, 'pathParameters': {'host_id': '75'},
 'stageVariables': {'developMode': 'dev', 'stage_name': 'api'}, 'body': None, 'isBase64Encoded': False}
