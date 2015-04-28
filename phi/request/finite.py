# -*- coding: utf-8 -*-
from phi.request.base import BaseRequest, CACHED_BODY_KEY


class FiniteRequest(BaseRequest):

    @property
    def content(self):
        if CACHED_BODY_KEY not in self._cache:
            content = None
            if self._content_stream is not None:
                content_length = self.content_length
                content = self._content_stream.read(content_length)
            self._cache[CACHED_BODY_KEY] = content
        return self._cache[CACHED_BODY_KEY]
