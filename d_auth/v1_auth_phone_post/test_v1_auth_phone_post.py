import logging
from datetime import datetime
from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from d_auth.v1_auth_phone_post.v1_auth_phone_post import lambda_handler

logger = logging.getLogger("api.test.v1_auth_phone_post")


class Test(TestCase):
    def test_signin_via_phone__with_no_matching_name(self):
        name = f'test_name_{datetime.now().timestamp()}'
        phoneNo = f'010-1234-1234'

        body = {
            'name': name,
            'phoneNo': phoneNo
        }

        try:
            json_body = Json.to_json_string(body)
            response = lambda_handler({'body': json_body}, {})

            logger.info(response)

            self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
        except Exception as exc:
            self.fail(exc)

    def test_signin_via_phone__with_matching_name(self):
        name = f'0_0woo__'
        phoneNo = f'010-5659-9706'

        body = {
            'name': name,
            'phoneNo': phoneNo
        }

        json_body = Json.to_json_string(body)
        response = lambda_handler({'body': json_body}, {})

        try:
            self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
        except Exception as exc:
            self.fail(exc)
        finally:
            logger.info(response)
