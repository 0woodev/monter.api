import logging
from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from common.const import ConstAWS
from d_user.v1_user_host_id_visitor_get.v1_user_host_id_visitor_get import lambda_handler

logger = logging.getLogger("api.test.place_visited_id_put")


class Test(TestCase):
    def test_lambda_handler(self):
        path = {
            "picture": None
        }

        response = lambda_handler({
            'headers': {
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0YmQtYWxwaGEudmVyY2VsLmFwcC8iLCJpYXQiOjE2ODE2OTkyNzYuMDM0OTE4LCJleHAiOjE2ODE3ODU2NzYuMDM0OTE4LCJpZCI6NiwibmFtZSI6ImZyb2dsaW1iZXIifQ.V3gdOV09M4lXbDMewFHh5YufPSkiCpaxMUYFIXWQfj8'
            },
            ConstAWS.PATH_PARAMETERS: {'host_id': '75'},
            ConstAWS.QUERY_PARAMETER: {'date': '2023-05-04'}
        }, {})

        try:
            body = Json.to_dict(response.get('body'))

            self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
            self.assertGreaterEqual(body['data']['day'], 0)
            self.assertGreaterEqual(body['data']['total'], 0)
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)
