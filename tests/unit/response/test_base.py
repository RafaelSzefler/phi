# -*- coding: utf-8 -*-
import pytest

from phi.response.base import BaseResponse
from phi.utils import CaseInsensitiveDict
from phi.constants import STATUSES

from tests.dependencies import mock

STATUS_EXAMPLES = list(STATUSES.items())
STATUS_EXAMPLES.append((777, "Unknown"))


class TestBaseResponse(object):

    @pytest.fixture
    def res(self):
        return BaseResponse()

    @pytest.mark.parametrize("key, value", [
        ("status", 200),
        ("content", None),
        ("charset", "utf-8"),
        ("content_type", "text/plain"),
        ("content_length", None),
        ("exception", None),
    ])
    def test_defaults(self, key, value):
        assert getattr(BaseResponse, key) == value

    def test___init__(self, res):
        assert isinstance(res.headers, CaseInsensitiveDict)

    @pytest.mark.parametrize("status, text", STATUS_EXAMPLES)
    def test__get_wsgi_status(self, status, text, res):
        result = "{status} {text}".format(
            status=status,
            text=text
        )
        res.status = status
        assert res._get_wsgi_status() == result

    def test__update_header_list_with_content_length(self, res):
        with pytest.raises(NotImplementedError):
            res._update_header_list_with_content_length([])

    @pytest.mark.parametrize("content_type, charset, result", [
        ("text", "utf-8", "text; charset=utf-8"),
        ("xyz", "blah", "xyz; charset=blah"),
        ("html/blah/foo", "xyz/test\z", "html/blah/foo; charset=xyz/test\z"),
    ])
    def test__get_full_content_type(self, content_type, charset, result, res):
        res.content_type = content_type
        res.charset = charset
        assert res._get_full_content_type() == result

    def test__update_header_list_with_headers(self, res):
        class CustomStr(object):
            def __str__(self):
                return "xyz"

        headers = []
        res.headers["test"] = 11
        res.headers["x_y-z"] = "test"
        res.headers["my-world"] = CustomStr()
        res._update_header_list_with_headers(headers)
        assert set(headers) == set([
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Test", "11"),
            ("My-World", "xyz"),
            ("X_y-Z", "test"),
        ])

    @mock.patch.object(
        BaseResponse,
        "_update_header_list_with_headers",
        new=lambda self, lst: lst.append(1)
    )
    @mock.patch.object(
        BaseResponse,
        "_update_header_list_with_content_length",
        new=lambda self, lst: lst.append(2)
    )
    def test__get_wsgi_headers(self, res):
        headers = res._get_wsgi_headers()
        assert headers == [1, 2]

    def test__get_wsgi_content_iterator(self, res):
        with pytest.raises(NotImplementedError):
            res._get_wsgi_content_iterator()
