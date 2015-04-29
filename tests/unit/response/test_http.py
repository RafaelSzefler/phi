# -*- coding: utf-8 -*-
import pytest

from phi.response.finite import FiniteResponse
from phi.response.http import HttpResponse


class TestHttpResponse(object):
    @pytest.fixture
    def http_res(self):
        return HttpResponse("ala ma kota")

    @pytest.mark.parametrize("base_cls", [FiniteResponse])
    def test_inheritance(self, base_cls, http_res):
        assert isinstance(http_res, base_cls)

    def test_defaults(self, http_res):
        assert http_res.content_type == "text/html"
        assert http_res.status == 200

    def test_default__init__(self, http_res):
        assert http_res.content == b"ala ma kota"
        assert http_res.content_length == len("ala ma kota")

    def test_content_type__init__(self):
        res = HttpResponse("test", content_type="xyz")
        assert res.content_type == "xyz"

    def test_status__init__(self):
        res = HttpResponse("test", status=300)
        assert res.status == 300
