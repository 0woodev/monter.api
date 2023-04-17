import datetime
from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from d_place.v1_place_visit_post.v1_place_visit_post import lambda_handler


class Test(TestCase):
    def test_lambda_handler(self):
        body = {
            'placeId': 6,
            'solvedLog': '쉬웠다리',
            # 'visitedAt': datetime.datetime(2023, 4, 10, 12, 15, 30, 0).isoformat()
            'visitedAt': 'Mon, 17 Apr 2023 03:21:28 GMT',
            'colorHex': '#D75353'
        }

        response = lambda_handler({
            'headers': {
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0YmQtYWxwaGEudmVyY2VsLmFwcC8iLCJpYXQiOjE2ODE2OTkyNzYuMDM0OTE4LCJleHAiOjE2ODE3ODU2NzYuMDM0OTE4LCJpZCI6NiwibmFtZSI6ImZyb2dsaW1iZXIifQ.V3gdOV09M4lXbDMewFHh5YufPSkiCpaxMUYFIXWQfj8'
            },
            'body': Json.to_json_string(body)
        }, {})

        new_place_user = Json.to_dict(response.get('body')).get("data")

        self.assertEqual(HTTPStatus.OK, response.get('statusCode'))
        self.assertEqual(6, new_place_user.get('userId'))
        self.assertEqual(body['placeId'], new_place_user.get('placeId'))

