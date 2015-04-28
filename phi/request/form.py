# -*- coding: utf-8 -*-
from six.moves.urllib.parse import unquote, parse_qs

from phi.request.base import CACHED_CONTENT_KEY
from phi.request.finite import FiniteRequest


class FormRequest(FiniteRequest):

    @property
    def content(self):
        if CACHED_CONTENT_KEY not in self._cache:
            body = self.body
            unquoted_body = unquote(body)
            parsed_body = parse_qs(unquoted_body)
            self._cache[CACHED_CONTENT_KEY] = parsed_body
        return self._cache[CACHED_CONTENT_KEY]
