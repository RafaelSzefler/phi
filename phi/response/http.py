# -*- coding: utf-8 -*-
from phi.response.finite import FiniteResponse


class HttpResponse(FiniteResponse):
    content_type = "text/html"

    def __init__(self, content, content_type=None, status=None):
        super(HttpResponse, self).__init__()
        self.content = content.encode(self.charset)
        self.content_length = len(self.content)
        if content_type:
            self.content_type = content_type
        if status:
            self.status = status
