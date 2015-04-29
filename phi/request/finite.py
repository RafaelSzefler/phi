# -*- coding: utf-8 -*-
from phi.request.base import BaseRequest


class FiniteRequest(BaseRequest):

    def _get_content(self):
        content = None
        if self._content_stream is not None:
            content_length = self.content_length
            content = self._content_stream.read(content_length)
            content = content.decode(self.charset)
        return content
