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
            'solvedLog': '🛑🛑🛑🛑',
            'visitedAt': '2023-04-19 19:37:34',
            'colorHex': '#D75354'
        }

        path_params = {
            'id': 47
        }

        response = lambda_handler({
            'headers': {
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0YmQtYWxwaGEudmVyY2VsLmFwcC8iLCJpYXQiOjE2ODE3ODY5MjQuNTcwNTA2LCJleHAiOjE2ODE4NzMzMjQuNTcwNTA2LCJpZCI6NiwibmFtZSI6ImFuZHkgbmFtIn0.WEl4pAafgnjSWs9CL2iLgMVbn--07xEtPWEKVSfz4Tw'
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
