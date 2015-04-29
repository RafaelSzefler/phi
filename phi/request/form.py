# -*- coding: utf-8 -*-

from phi.request.finite import FiniteRequest
from phi.utils import parse_query_string


class FormRequest(FiniteRequest):

    def _get_body(self):
        return parse_query_string(self.content)
