# -*- coding: utf-8 -*-
from io import BytesIO

import pytest

from phi.request.finite import FiniteRequest


@pytest.fixture
def stream():
    io_stream = BytesIO("ala ma kota")
    io_stream.seek(0)
    return io_stream


class TestFiniteRequest(object):
    @pytest.fixture
    def fin_req(self):
        return FiniteRequest()

    def test_null_body(self, fin_req):
        assert fin_req.body is None

    def test_body_stream(self, fin_req, stream):
        fin_req._content_stream = stream
        fin_req.content_length = 11
        assert fin_req.body == "ala ma kota"

    def test_short_length_body_stream(self, fin_req, stream):
        fin_req._content_stream = stream
        fin_req.content_length = 4
        assert fin_req.body == "ala "
