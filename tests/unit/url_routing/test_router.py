# -*- coding: utf-8 -*-
import pytest

from phi.exceptions import RoutingException, HttpNotFound
from phi.request.base import BaseRequest
from phi.url_routing.pattern import PatternBuilder, Pattern
from phi.url_routing.router import URLRouter

from tests.dependencies import mock


@pytest.fixture(scope="function")
def url_router():
    return URLRouter()


class TestURLRouter(object):
    def test__init__(self, url_router):
        assert url_router._handlers == {}
        assert url_router._patterns == []

    @mock.patch.object(URLRouter, "get_handler_and_params_from_url")
    def test_get_handler_and_params_from_request(self, m_get, url_router):
        req = mock.Mock(spec=BaseRequest)
        handle = url_router.get_handler_and_params_from_request(req)
        m_get.assert_called_once_with(req.url)
        assert handle == m_get(req.url)

    @mock.patch.object(PatternBuilder, "from_simple_pattern", return_value=1)
    def test_add_route(self, m_from, url_router):
        my_fn = mock.Mock()
        url_router.add_route("test", "/", my_fn)
        assert url_router._handlers == {"test": ("test", 1, my_fn)}

    @mock.patch.object(PatternBuilder, "from_simple_pattern", return_value=1)
    def test_add_route_exists(self, m_from, url_router):
        my_fn = mock.Mock()
        my_fn_2 = mock.Mock()
        url_router.add_route("test", "/", my_fn)
        with pytest.raises(RoutingException):
            url_router.add_route("test", "/2", my_fn_2)

    def test_reverse_no_key(self, url_router):
        with pytest.raises(KeyError):
            url_router.reverse("test")

    @mock.patch.object(PatternBuilder, "from_simple_pattern")
    def test_reverse(self, m_from_regex, url_router):
        pattern = mock.Mock(spec=Pattern)
        m_from_regex.return_value = pattern
        my_fn = mock.Mock()
        url_router.add_route("test", "/{x}", my_fn)
        params = {"x": 1}
        url = url_router.reverse("test", params=params)
        pattern.reverse.assert_called_once_with(params)
        assert url == pattern.reverse(params)

    def test_get_handler_and_params_from_url(self, url_router):
        pattern_1 = mock.Mock(spec=Pattern)
        pattern_1.match.return_value = (False, None)
        pattern_2 = mock.Mock(spec=Pattern)
        pattern_2.match.return_value = (True, {"test": 1})
        pattern_3 = mock.Mock(spec=Pattern)
        pattern_3.match.return_value = (True, {"foo": "bar"})
        url_router._patterns = [
            ("test", pattern_1, "xyz"),
            ("test2", pattern_2, "blah"),
            ("test3", pattern_3, "super"),
        ]

        handler, params = url_router.get_handler_and_params_from_url("/")
        assert handler == "blah"
        assert params == {"test": 1}
        pattern_1.match.assert_called_once_with("/")
        pattern_2.match.assert_called_once_with("/")
        assert not pattern_3.match.called

    def test_get_handler_and_params_from_url_not_found(self, url_router):
        pattern_1 = mock.Mock(spec=Pattern)
        pattern_1.match.return_value = (False, None)
        pattern_2 = mock.Mock(spec=Pattern)
        pattern_2.match.return_value = (False, {"test": 1})
        pattern_3 = mock.Mock(spec=Pattern)
        pattern_3.match.return_value = (False, {"foo": "bar"})
        url_router._patterns = [
            ("test", pattern_1, "xyz"),
            ("test2", pattern_2, "blah"),
            ("test3", pattern_3, "super"),
        ]

        with pytest.raises(HttpNotFound):
            url_router.get_handler_and_params_from_url("/")
