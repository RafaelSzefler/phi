# -*- coding: utf-8 -*-
from six.moves.urllib.parse import unquote, parse_qs

from phi.request.finite import FiniteRequest


class FormRequest(FiniteRequest):

    def _get_body(self):
        content = self.content
        unquoted_body = unquote(content)
        return parse_qs(unquoted_body)
