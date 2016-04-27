# -*- coding: utf-8 -*-
from phi.dependencies import msgpack
from phi.response.finite import FiniteResponse


class MsgpackResponse(FiniteResponse):
    content_type = "application/msgpack"

    def __init__(self, content, status=None):
        super(MsgpackResponse, self).__init__()
        if msgpack is None:
            raise ImportError('msgpack not available')
        self.content = msgpack.packb(content)
        self.content_length = len(self.content)
        if status:
            self.status = status
