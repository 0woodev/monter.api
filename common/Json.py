import json
import enum
from decimal import Decimal


class ClsJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, object):
                if hasattr(obj, "__dict__"):
                    return obj.__dict__
                else:
                    return str(obj)
            else:
                return json.JSONEncoder.default(self, obj)
        except Exception as exception:
            raise exception


class Json:
    @classmethod
    def to_dict(cls, string: str):
        return json.loads(string)

    @classmethod
    def to_json_string(cls, obj: object, **kwargs):
        try:
            return json.dumps(obj, cls=ClsJsonEncoder, ensure_ascii=False, **kwargs)
        except Exception as exception:
            raise exception
