import logging
from datetime import datetime
from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from d_auth.v1_auth_signin_post.v1_auth_signin_post import lambda_handler

logger = logging.getLogger("api.test.v1_auth_signin_post")


class Test(TestCase):
    def test_signin_fail_with_no_matching_name(self):
        name = f'test_name_{datetime.now().timestamp()}'
        password = f'password'

        body = {
            'name': name,
            'password': password
        }

        json_body = Json.to_json_string(body)
        response = lambda_handler({'body': json_body}, {})

        try:
            self.assertEqual(HTTPStatus.BAD_REQUEST, response.get('statusCode'))
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)

    def test_signin(self):
        name = f'test_name_hi'
        password = f'password'

        body = {
            'name': name,
            'password': password
        }
        json_body = Json.to_json_string(body)
        response = lambda_handler({'body': json_body}, {})

        try:
            self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)


    def test_signin_fail_with_wrong_password(self):
        name = f'test_name_hi'
        password = f'password1'

        body = {
            'name': name,
            'password': password
        }
        json_body = Json.to_json_string(body)
        response = lambda_handler({'body': json_body}, {})

        try:
            self.assertEqual(HTTPStatus.BAD_REQUEST, response.get('statusCode'))
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)

