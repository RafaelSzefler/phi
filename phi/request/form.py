# -*- coding: utf-8 -*-
from six.moves.urllib.parse import unquote, parse_qs

from phi.request.base import CACHED_CONTENT_KEY
from phi.request.finite import FiniteRequest


class FormRequest(FiniteRequest):

    @property
    def body(self):
        if CACHED_CONTENT_KEY not in self._cache:
            content = self.content
            unquoted_body = unquote(content)
            body = parse_qs(unquoted_body)
            self._cache[CACHED_CONTENT_KEY] = body
        return self._cache[CACHED_CONTENT_KEY]
