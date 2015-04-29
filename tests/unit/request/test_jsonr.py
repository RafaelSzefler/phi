# -*- coding: utf-8 -*-
import pytest

from io import BytesIO

from phi.request.jsonr import JsonRequest


@pytest.fixture
def stream():
    io_stream = BytesIO(b'{"test": 1, "foo":  "bar"}')
    io_stream.seek(0)
    return io_stream


class TestJsonRequest(object):
    def test_body(self, stream):
        req = JsonRequest()
        req._content_stream = stream
        assert req._get_body() == {"test": 1, "foo": "bar"}
