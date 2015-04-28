# -*- coding: utf-8 -*-
import pytest

from phi.request.base import BaseRequest
from phi.utils import CaseInsensitiveDict

from tests.utils import mock


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

    @pytest.mark.parametrize("attr", ["body", "content_iterator", "content"])
    def test_not_implemented_properties(self, attr, req):
        with pytest.raises(NotImplementedError):
            getattr(req, attr)

    @pytest.mark.parametrize("attr", ["_get_body", "_get_content"])
    def test_not_implemented_fns(self, attr, req):
        with pytest.raises(NotImplementedError):
            fn = getattr(req, attr)
            fn()

    @pytest.mark.parametrize("attr", ["body", "content"])
    def test_data_caching(self, attr, req):
        with mock.patch.object(BaseRequest, "_get_"+attr) as mocked:
            data = getattr(req, attr)
            assert mocked.called
            data2 = getattr(req, attr)
            assert mocked.call_count == 1
            assert data2 is data

    @pytest.mark.parametrize("header, result", [
        (None, False),
        ("blah", False),
        ("XMLHttpRequest", True),
        ("xmlhttprequest", True)
    ])
    def test_is_ajax(self, header, result, req):
        req.headers["X-Requested-With"] = header
        assert req.is_ajax() is result
