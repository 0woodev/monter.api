import logging
from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from common.const import ConstAWS
from d_user.v1_user_host_id_visitor_post.v1_user_host_id_visitor_post import lambda_handler

logger = logging.getLogger("api.test.place_visited_id_put")


class Test(TestCase):
    def test_lambda_handler(self):
        body = {
            "date": "2023-05-04"
        }

        response = lambda_handler({
            'body': Json.to_json_string(body),
            ConstAWS.PATH_PARAMETERS: {'host_id': '75'}
        }, {})

        try:
            self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)
