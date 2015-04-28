# -*- coding: utf-8 -*-
from phi.dependencies import json
from phi.request.base import CACHED_CONTENT_KEY
from phi.request.finite import FiniteRequest


class JsonRequest(FiniteRequest):

    @property
    def content(self):
        if CACHED_CONTENT_KEY not in self._cache:
            body = self.body
            content = json.loads(body)
            self._cache[CACHED_CONTENT_KEY] = content
        return self._cache[CACHED_CONTENT_KEY]
