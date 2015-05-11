# -*- coding: utf-8 -*-
import pytest

from phi.app import Application
from phi.defaults.exception_handler import default_exception_handler
from phi.exceptions import HttpException, HttpNotFound
from phi.request.base import BaseRequest
from phi.request.builder import RequestBuilder
from phi.response.base import BaseResponse
from phi.url_routing.router import URLRouter

from tests.dependencies import mock


class TestApp(object):
    def test_init_default(self):
        Application()

    def test_init_custom_request_builder_factory(self):
        custom_factory = lambda: mock.sentinel.request_builder
        app = Application(request_builder_factory=custom_factory)
        assert app._request_builder == mock.sentinel.request_builder

    @mock.patch.object(URLRouter, "get_handler_and_params_from_request")
    def test__get_handler_and_params(self, m_get, app, request):
        req = mock.Mock(spec=BaseRequest)
        result = app._get_handler_and_params(req)
        m_get.assert_called_once_with(req)
        assert result == m_get(req)

    @mock.patch.object(URLRouter, "get_handler_and_params_from_request")
    def test__get_handler_and_params_exc(self, m_get, app, request):
        m_get.side_effect = HttpNotFound
        req = mock.Mock(spec=BaseRequest)
        result = app._get_handler_and_params(req)
        m_get.assert_called_once_with(req)
        assert result == (
            default_exception_handler,
            {
                "exc": None,
                "status": 404
            }
        )

    @mock.patch.object(URLRouter, "get_handler_and_params_from_request")
    def test__get_handler_and_params_exc_no_handler(self, m_get, app, request):
        def revert():
            app._exception_handler = default_exception_handler
        request.addfinalizer(revert)
        app._exception_handler = None
        m_get.side_effect = HttpNotFound
        req = mock.Mock(spec=BaseRequest)
        with pytest.raises(HttpNotFound):
            app._get_handler_and_params(req)
        m_get.assert_called_once_with(req)

    @mock.patch("phi.app.get_status_from_exc")
    def test__handle_exception(self, m_get, app, request):
        def revert():
            app._exception_handler = default_exception_handler
        request.addfinalizer(revert)

        m_get.return_value = 123
        m_exc = mock.Mock()
        app._exception_handler = m_exc

        req = mock.Mock(spec=BaseRequest)
        exc = mock.Mock()
        result = app._handle_exception(req, exc)
        m_exc.assert_called_once_with(req, exc, 123)
        m_get.assert_called_once_with(exc)
        assert result == m_exc(req, exc, 123)

    @mock.patch("phi.app.get_status_from_exc")
    def test__handle_exception_no_handler(self, m_get, app, request):
        def revert():
            app._exception_handler = default_exception_handler
        request.addfinalizer(revert)

        m_get.return_value = 123
        app._exception_handler = None

        req = mock.Mock(spec=BaseRequest)
        exc = None
        try:
            0/0
        except Exception as e:
            exc = e
            with pytest.raises(ZeroDivisionError):
                app._handle_exception(req, e)
        m_get.assert_called_once_with(exc)

    def test__preprocess(self, app, request):
        def revert():
            app._middleware = None
        request.addfinalizer(revert)

        app._middleware = mock.Mock()
        request = mock.Mock()
        res = app._preprocess(request)
        assert res == app._middleware.preprocess(request)

    @mock.patch.object(Application, "_handle_exception")
    def test__preprocess_exc(self, m_exc, app, request):
        def revert():
            app._middleware = None
        request.addfinalizer(revert)

        app._middleware = mock.Mock()
        exc = Exception()
        app._middleware.preprocess.side_effect = exc
        request = mock.Mock()
        res = app._preprocess(request)
        m_exc.assert_called_once_with(request, exc)
        assert res == m_exc(request, exc)

    def test__preprocess_no_middle(self, app, request):
        request = mock.Mock()
        res = app._preprocess(request)
        assert res is None

    @mock.patch.object(Application, "_handle_exception")
    def test__postprocess(self, m_exc, app, request):
        def revert():
            app._middleware = None
        request.addfinalizer(revert)

        app._middleware = mock.Mock()
        exc = Exception()
        app._middleware.postprocess.side_effect = exc
        request = mock.Mock()
        response = mock.Mock()
        res = app._postprocess(request, response)
        m_exc.assert_called_once_with(request, exc)
        assert res == m_exc(request, exc)

    def test__postprocess_exc(self, app, request):
        def revert():
            app._middleware = None
        request.addfinalizer(revert)

        app._middleware = mock.Mock()
        request = mock.Mock()
        response = mock.Mock()
        res = app._postprocess(request, response)
        assert res == app._middleware.postprocess(request, response)

    def test__postprocess_no_middle(self, app, request):
        request = mock.Mock()
        response = mock.Mock()
        res = app._postprocess(request, response)
        assert res is response

    @mock.patch.object(Application, "_postprocess")
    @mock.patch.object(Application, "_preprocess")
    def test__get_response_ok(self, m_pre, m_post, app):
        response = mock.Mock()
        m_pre.return_value = None
        m_post.return_value = response

        def handler(req, **kwargs):
            return response

        request = mock.Mock(spec=BaseRequest)
        params = {}
        assert app._get_response(handler, request, params) == response
        m_pre.assert_called_once_with(request)
        m_post.assert_called_once_with(request, response)

    @mock.patch.object(Application, "_preprocess")
    def test__get_response_preprocess(self, m_pre, app):
        response = mock.Mock()
        preresponse = mock.Mock()
        m_pre.return_value = preresponse

        def handler(req, **kwargs):
            return response

        request = mock.Mock(spec=BaseRequest)
        params = {}
        real_response = app._get_response(handler, request, params)
        m_pre.assert_called_once_with(request)
        assert real_response == preresponse

    @mock.patch.object(Application, "_handle_exception")
    def test__get_response_http_error(self, m_handle, app):
        exc = HttpException()
        exc.status = 401

        def handler(req, test):
            raise exc

        req = mock.Mock(spec=BaseRequest)
        params = {"test": 11}

        res = app._get_response(handler, req, params)
        m_handle.assert_called_once_with(req, exc)
        assert res == m_handle(req, exc)

    @mock.patch.object(Application, "_handle_exception")
    def test__get_response_other_error(self, m_handle, app):
        exc = Exception()

        def handler(req, test):
            raise exc

        req = mock.Mock(spec=BaseRequest)
        params = {"test": 11}

        res = app._get_response(handler, req, params)
        m_handle.assert_called_once_with(req, exc)
        assert res == m_handle(req, exc)

    def test__start_response(self, app):
        res = mock.Mock(spec=BaseResponse)
        res._get_wsgi_status.return_value = "200 Test"
        res._get_wsgi_headers.return_value = [("Content-Type", "Test")]

        start_response = mock.Mock()

        app._start_response(res, start_response)
        start_response.assert_called_once_with(
            "200 Test", [("Content-Type", "Test")]
        )

    @mock.patch.object(RequestBuilder, "build_request_from_env")
    @mock.patch.object(Application, "_get_handler_and_params")
    @mock.patch.object(Application, "_get_response")
    @mock.patch.object(Application, "_start_response")
    def test_handle_wsgi_request(self, m_send, m_resp, m_handle, m_build, app):
        req = mock.Mock(spec=BaseRequest)
        start_response = mock.Mock()
        resp = mock.Mock(spec=BaseResponse)
        resp._get_wsgi_content_iterator.return_value = [1, 2, 3]
        m_resp.return_value = resp
        m_handle.return_value = ("test", "test")
        result = list(app.handle_wsgi_request(req, start_response))
        assert result == [1, 2, 3]
        for mocked in [m_send, m_resp, m_handle, m_build]:
            assert mocked.call_count == 1

    def test_call(self):
        assert Application.__call__ == Application.handle_wsgi_request
