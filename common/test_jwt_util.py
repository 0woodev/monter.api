import traceback
from unittest import TestCase

from common.MonterException import MonterException
from common.jwt_util import generate_jwt_token, decode_jwt_token


class Test(TestCase):
    def test_generate_jwt_token(self):
        user_id = 75
        name = '0_0woo__'

        try:
            token = generate_jwt_token(user_id, name)
            print(token)
        except Exception as exc:
            self.fail(exc)

    def test_decode_jwt_token(self):
        # if sample token is invalid, make new token through above test code, and then switch
        sample_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0YmQtYWxwaGEudmVyY2VsLmFwcC8iLCJpYXQiOjE2ODE3ODY5MjQuNTcwNTA2LCJleHAiOjE2ODE4NzMzMjQuNTcwNTA2LCJpZCI6NiwibmFtZSI6ImFuZHkgbmFtIn0.WEl4pAafgnjSWs9CL2iLgMVbn--07xEtPWEKVSfz4Tw'

        expect_user_id = 6
        expect_name = 'andy nam'

        try:
            payload = decode_jwt_token(sample_token)

            self.assertEquals(expect_user_id, payload.get('id'))
            self.assertEquals(expect_name, payload.get('name'))
        except MonterException as exc:
            self.fail(f"{exc.result_code.status_code_string} {exc.data}")
        except Exception as exc:
            self.fail(f"why...? {traceback.format_exc()}")



