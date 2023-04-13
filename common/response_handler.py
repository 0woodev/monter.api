from http import HTTPStatus
import logging

from common.response_builder import build_response, build_fail_response

logger = logging.getLogger("api.response_handler")


def _api_handler(func):
    # @wraps(f)
    def wrapper(*args, **kwargs):
        event = args[0]
        context = args[1]
        logger.info(event)
        try:
            response_data = func(event, context)
            response = build_response(response_data)
        except Exception as exc:
            response = build_fail_response(exc)

        return response

    return wrapper


class ResponseHandler:
    api = _api_handler
