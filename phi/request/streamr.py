# -*- coding: utf-8 -*-
from phi.request.base import BaseRequest


class StreamRequest(BaseRequest):

    @property
    def content_iterator(self):
        pass  # TODO
