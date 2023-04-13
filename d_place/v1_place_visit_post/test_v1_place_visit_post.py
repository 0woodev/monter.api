import datetime
from http import HTTPStatus
from unittest import TestCase

from common.Json import Json
from d_place.v1_place_visit_post.v1_place_visit_post import lambda_handler


class Test(TestCase):
    def test_lambda_handler(self):
        body = {
            "placeId": 6,
            "solvedLog": "쉬웠다리",
            "visitedAt": datetime.datetime(2023, 4, 10, 12, 15, 30, 0).isoformat()
        }

        response = lambda_handler({
            "headers": {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NiwibmFtZSI6ImFuZHkgbmFtIiwiaWF0IjoxNjgwODA0Njk0LCJleHAiOjE2ODMzOTY2OTR9.B_i9nDTgjy6MMY6bgIUeYt3RdKdeQnjgRMY47oZBfeA"
            },
            "body": Json.to_json_string(body)
        }, {})

        self.assertEquals(HTTPStatus.OK, response.get("statusCode"))

