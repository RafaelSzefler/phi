# -*- coding: utf-8 -*-
from phi.dependencies import json
from phi.request.finite import FiniteRequest


class JsonRequest(FiniteRequest):

    def _get_body(self):
        content = self.content
        return json.loads(content)
