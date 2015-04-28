# -*- coding: utf-8 -*-
from phi.dependencies import json
from phi.request.base import CACHED_CONTENT_KEY
from phi.request.finite import FiniteRequest


class JsonRequest(FiniteRequest):

    @property
    def body(self):
        if CACHED_CONTENT_KEY not in self._cache:
            content = self.content
            body = json.loads(content)
            self._cache[CACHED_CONTENT_KEY] = body
        return self._cache[CACHED_CONTENT_KEY]
