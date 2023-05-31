import logging
import random

from twilio.rest import Client

from common.CommonResultCode import CommonResultCode
from common.Json import Json
from common.MonterException import MonterException
from common.const import ConstTwilio
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')

client = Client(ConstTwilio.ACCOUNT_SID, ConstTwilio.AUTH_TOKEN)


@ResponseHandler.api
def lambda_handler(event, context):
    phone_no = get_body_contents(event)

    code = make_random_4_digits()
    message = ConstTwilio.MESSAGE_FORMAT.format(code=code)

    phone_no = f"+82{phone_no}"
    twilio_response = send_trailio_sms(phone_no, message)

    if twilio_response.get('statusCode', 400) != 200:
        raise MonterException(CommonResultCode.TWILIO_SEND_SMS_ERROR, None, twilio_response['errorMessage'])

    return { 'code': code }


def get_body_contents(event) -> str:
    body_dict = Json.to_dict(event['body'])

    if 'phoneNo' not in body_dict:
        raise MonterException(CommonResultCode.INVALID_BODY_CONTENTS, None, '휴대폰 번호가 없습니다')

    return body_dict['phoneNo']


def make_random_4_digits() -> int:
    return random.randint(1000, 10000)


def send_trailio_sms(to, contents):
    message = client.messages.create(
        from_=ConstTwilio.FROM,
        body=contents,
        to=to
    )

    status_code = 200 if message.error_code is None else message.error_code
    return {
        'statusCode': status_code,
        'errorMessage': message.error_message,
        'message.sid': message.sid
    }
