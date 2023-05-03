from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from common.const import ConstAWS
from d_user.v1_user_verified_post.v1_user_verified_post import lambda_handler

import requests
from bs4 import BeautifulSoup

import logging

logger = logging.getLogger("api.test.v1_user_verified_post")


class Test(TestCase):
    def test_lambda_handler(self):

        response = lambda_handler({
            'headers': {
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0YmQtYWxwaGEudmVyY2VsLmFwcC8iLCJpYXQiOjE2ODMwOTg4OTcuNjE4OTI1LCJleHAiOjE2ODU2OTA4OTcuNjE4OTI1LCJpZCI6NzUsIm5hbWUiOiIwXzB3b29fXyJ9.5OLKSVUL9NC436m5zTdN1nJY7nN0rIGUXmExo_5PieY'
            },
        }, {})

        try:
            self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)
