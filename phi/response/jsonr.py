# -*- coding: utf-8 -*-
from phi.dependencies import json
from phi.response.finite import FiniteResponse


class JsonResponse(FiniteResponse):
    content_type = "application/json"

    def __init__(self, content, status=None):
        super(JsonResponse, self).__init__()
        content = json.dumps(content, separators=(',', ':'))
        self.content = content.encode(self.charset)
        self.content_length = len(self.content)
        if status:
            self.status = status
