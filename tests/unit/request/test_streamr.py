# -*- coding: utf-8 -*-
from phi.request.streamr import StreamRequest


class TestStreamRequest(object):

    def test_content_iterator(self):
        req = StreamRequest()
        req.content_iterator  # TODO
