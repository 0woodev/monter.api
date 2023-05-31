import logging
from datetime import datetime
from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from d_auth.v1_auth_sms_code_post.v1_auth_sms_code_post import lambda_handler

logger = logging.getLogger("api.test.v1_auth_sms_code_post")


class Test(TestCase):
    def test_send_sms_via_twilio(self):
        phoneNo = '01056599706'

        body = {
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

