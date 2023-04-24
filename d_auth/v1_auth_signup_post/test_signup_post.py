import logging
from datetime import datetime
from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from d_auth.v1_auth_signup_post.v1_auth_signup_post import lambda_handler

logger = logging.getLogger("api.test.v1_auth_signup_post")


class Test(TestCase):
    def test_signup_with_new_name(self):
        name = f'test_name_{datetime.now().timestamp()}'
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

    def test_fail_with_exist_name(self):
        name = f'test_name_{datetime.now().timestamp()}'
        password = f'password'

        body = {
            'name': name,
            'password': password
        }
        json_body = Json.to_json_string(body)
        response = lambda_handler({'body': json_body}, {})

        response2 = lambda_handler({'body': json_body}, {})

        try:
            self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
            self.assertEqual(HTTPStatus.BAD_REQUEST, response2.get('statusCode'))
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)

    def test_make_test_user_for_signin_test(self):
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

