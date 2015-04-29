# -*- coding: utf-8 -*-
from phi.request.multipart import MultipartRequest


class TestMultipartRequest(object):

    def test_content_iterator(self):
        req = MultipartRequest()
        req.content_iterator  # TODO
