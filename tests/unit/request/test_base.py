# -*- coding: utf-8 -*-
import pytest

from phi.request.base import BaseRequest
from phi.utils import CaseInsensitiveDict


class TestBaseRequest(object):
    @pytest.fixture
    def req(self):
        return BaseRequest()

    @pytest.mark.parametrize("key, value", [
        ("env", None),
        ("method", None),
        ("url", None),
        ("url_scheme", None),
        ("content_type", None),
        ("content_length", None),
        ("query_string", None),
        ("remote_user", None),
        ("remote_addr", None),
        ("_content_stream", None)
    ])
    def test_constants(self, key, value):
        assert getattr(BaseRequest, key) == value

    def test__init__(self, req):
        assert isinstance(req.headers, CaseInsensitiveDict)
        assert req.query_params == {}
        assert req._cache == {}

    @pytest.mark.parametrize("attr", ["body", "body_iterator", "content"])
    def test_not_implemented_properties(self, attr, req):
        with pytest.raises(NotImplementedError):
            getattr(req, attr)
