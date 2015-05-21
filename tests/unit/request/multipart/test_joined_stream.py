# -*- coding: utf-8 -*-
from io import BytesIO

import pytest

from phi.request.multipart.joined_stream import JoinedStream


class TestJoinedStream(object):
    @pytest.fixture
    def joined_stream(self):
        streams = [
            BytesIO(b"test "),
            BytesIO(b" ala"),
            BytesIO(b" xyz")
        ]
        return JoinedStream(streams)

    @pytest.mark.parametrize("size, result", [
        (4, b"test"),
        (6, b"test  "),
        (8, b"test  al"),
        (11, b"test  ala x"),
        (13, b"test  ala xyz"),
        (20, b"test  ala xyz")
    ])
    def test_read(self, size, result, joined_stream):
        assert joined_stream.read(size) == result
