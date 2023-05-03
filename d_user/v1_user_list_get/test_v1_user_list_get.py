import logging
from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from d_user.v1_user_list_get.v1_user_list_get import lambda_handler

logger = logging.getLogger("api.test.place_visited_id_put")


class Test(TestCase):
    def test_lambda_handler(self):
        body = {
            "picture": None
        }

        response = lambda_handler({
            'headers': {
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0YmQtYWxwaGEudmVyY2VsLmFwcC8iLCJpYXQiOjE2ODE2OTkyNzYuMDM0OTE4LCJleHAiOjE2ODE3ODU2NzYuMDM0OTE4LCJpZCI6NiwibmFtZSI6ImZyb2dsaW1iZXIifQ.V3gdOV09M4lXbDMewFHh5YufPSkiCpaxMUYFIXWQfj8'
            },
            'body': Json.to_json_string(body)
        }, {})

        try:
            self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)
