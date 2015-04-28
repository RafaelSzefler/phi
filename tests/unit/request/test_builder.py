# -*- coding: utf-8 -*-
import pytest

from phi.request.builder import RequestBuilder
from phi.request.base import BaseRequest
from phi.request.finite import FiniteRequest
from phi.request.form import FormRequest
from phi.request.jsonr import JsonRequest
from phi.request.streamr import StreamRequest

from tests.utils import mock


@pytest.fixture(scope="module")
def builder():
    return RequestBuilder()


class TestRequestBuilder(object):
    def test__build_headers(self, builder):
        env = {
            "HTTP_TEST": "test",
            "wsgi.url_scheme": "HTTPS",
            "REQUEST_METHOD": "GET",
            "CONTENT_TYPE": "blah",
            "CONTENT_LENGTH": "111",
            "QUERY_STRING": "xyz=11&foo=bar&foo=baz",
            "HTTP_ACCEPT": "foo",
            "HTTP_MY_CUSTOM_HEADER": "baz"
        }
        req = BaseRequest()
        builder._build_headers(req, env)
        assert req.headers == {
            "test": "test",
            "accept": "foo",
            "my-custom-header": "baz"
        }

    def test__build_constant_keys(self, builder):
        env = {
            "PATH_INFO": "/test",
            "wsgi.url_scheme": "HTTPS",
            "REQUEST_METHOD": "GET",
            "CONTENT_TYPE": "blah",
            "CONTENT_LENGTH": "111",
            "QUERY_STRING": "xyz=11&foo=bar&foo=baz",
            "wsgi.input": 1
        }
        req = BaseRequest()
        builder._build_constant_keys(req, env)
        assert req.env is env
        assert req.url == "/test"
        assert req.url_scheme == "HTTPS"
        assert req.method == "GET"
        assert req.content_type == "blah"
        assert req.content_length == 111
        assert req.query_string == "xyz=11&foo=bar&foo=baz"
        assert req.query_params == {"xyz": ["11"], "foo": ["bar", "baz"]}
        assert req.remote_user is None
        assert req.remote_addr is None
        assert req._content_stream == 1

    def test__build_constant_keys_missing_some_keys(self, builder):
        env = {
            "PATH_INFO": "/test",
            "wsgi.url_scheme": "HTTPS",
            "REQUEST_METHOD": "GET",
            "CONTENT_TYPE": "blah",
        }
        req = BaseRequest()
        builder._build_constant_keys(req, env)
        assert req.env is env
        assert req.url == "/test"
        assert req.url_scheme == "HTTPS"
        assert req.method == "GET"
        assert req.content_type == "blah"
        assert req.content_length is None
        assert req.query_string is None
        assert req.query_params == {}
        assert req.remote_user is None
        assert req.remote_addr is None

    @pytest.mark.parametrize("env, req_cls", [
        ({}, StreamRequest),
        ({"CONTENT_LENGTH": 1}, FiniteRequest),
        ({"CONTENT_LENGTH": 1, "CONTENT_TYPE": "application/json"}, JsonRequest),
        ({"CONTENT_TYPE": "application/json"}, StreamRequest),
        ({"CONTENT_LENGTH": 3, "CONTENT_TYPE": "application/x-www-form-urlencoded"}, FormRequest)
    ])
    def test__get_request_class_from_env(self, env, req_cls, builder):
        request_class = builder._get_request_class_from_env(env)
        assert request_class is req_cls

    @mock.patch.object(RequestBuilder, "_get_request_class_from_env")
    @mock.patch.object(RequestBuilder, "_build_constant_keys")
    @mock.patch.object(RequestBuilder, "_build_headers")
    def test_build_request_from_env(self, m_head, m_const, m_inst, builder):
        env = mock.Mock()
        req = builder.build_request_from_env(env)
        m_inst.assert_called_once_with(env)
        built_req_cls = m_inst(env)
        built_req = built_req_cls()
        m_const.assert_called_once_with(built_req, env)
        m_head.assert_called_once_with(built_req, env)
        assert req == built_req
