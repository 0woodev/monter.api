from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from common.const import ConstAWS
from d_place.v1_place_visited_id_put.v1_place_visited_id_put import lambda_handler

import logging

logger = logging.getLogger("api.test.place_visited_id_put")


class Test(TestCase):
    def test_lambda_handler(self):
        body = {
            'solvedLog': '바뀌어라',
            # 'visitedAt': '2023-04-08 19:37:34',
            'colorHex': '#D75353'
        }

        path_params = {
            'id': 5
        }

        response = lambda_handler({
            'headers': {
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0YmQtYWxwaGEudmVyY2VsLmFwcC8iLCJpYXQiOjE2ODE2OTkyNzYuMDM0OTE4LCJleHAiOjE2ODE3ODU2NzYuMDM0OTE4LCJpZCI6NiwibmFtZSI6ImZyb2dsaW1iZXIifQ.V3gdOV09M4lXbDMewFHh5YufPSkiCpaxMUYFIXWQfj8'
            },
            ConstAWS.PATH_PARAMETERS: path_params,
            'body': Json.to_json_string(body)
        }, {})


        try:
            self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)
