# -*- coding: utf-8 -*-
from phi.request.streamr import StreamRequest


class TestStreamRequest(object):

    def test_body_iterator(self):
        req = StreamRequest()
        req.body_iterator  # TODO
