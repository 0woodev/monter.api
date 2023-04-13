from __future__ import annotations

import inspect
from common.ResultCode import ResultCode


class MonterException(RuntimeError):
    def __init__(self, result_code: ResultCode, exception: Exception | None, data: str = None, *args, **kwargs):
        """

        :rtype: object
        """
        super().__init__(exception, result_code, data)

        self.result_code = result_code
        self.exception = exception
        self.context = inspect.stack()
        self.args = args
        self.kwargs = kwargs
        self.parameters = args

        if exception is not None:
            self.args = (*exception.args, *args)

        if isinstance(exception, MonterException):
            self.kwargs = {**exception.kwargs, **kwargs}

        if data is not None:
            self.data = data
        else:
            self.data = result_code.message
