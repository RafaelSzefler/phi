# -*- coding: utf-8 -*-
from phi.dependencies import json
from phi.response.base import BaseResponse, FiniteResponseMixin


class JsonResponse(FiniteResponseMixin, BaseResponse):
    content_type = "application/json"

    def __init__(self, content, status=None):
        super(JsonResponse, self).__init__()
        self.content = json.dumps(content, encoding=self.charset)
        self.content_length = len(self.content)
        if status:
            self.status = status
