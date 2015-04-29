# -*- coding: utf-8 -*-
from phi.defaults import default_exception_handler
from phi.exceptions import HttpNotFound
from phi.request.builder import RequestBuilder
from phi.utils import get_status_from_exc


NOT_FOUND_PARAMS = {
    "exc": None,
    "status": 404
}


class Application(object):
    def __init__(
        self,
        url_router=None,
        middleware_handler=None,
        request_builder_factory=RequestBuilder,
        exception_handler=default_exception_handler
    ):
        self._url_router = url_router
        self._middleware_handler = middleware_handler
        self._request_builder = request_builder_factory()
        self._exception_handler = exception_handler

    def handle_wsgi_request(self, env, start_response):
        request = self._request_builder.build_request_from_env(env)
        handler, params = self._get_handler_and_params(request)
        response = self._get_response(handler, request, params)
        self._start_response(response, start_response)
        for chunk in response._get_wsgi_content_iterator():
            yield chunk

    def _get_handler_and_params(self, request):
        try:
            return self._url_router.get_handler_and_params_from_request(
                request
            )
        except HttpNotFound:
            return self._exception_handler, NOT_FOUND_PARAMS

    def _get_response(self, handler, request, params):
        response = self._preprocess(request)
        if response:
            return response

        try:
            response = handler(request, **params)
        except Exception as e:
            response = self._handle_exception(request, e)

        response = self._postprocess(request, response)
        return response

    def _preprocess(self, request):
        if not self._middleware_handler:
            return None

        try:
            return self._middleware_handler.preprocess(request)
        except Exception as e:
            return self._handle_exception(request, e)

    def _postprocess(self, request, response):
        if not self._middleware_handler:
            return response

        try:
            return self._middleware_handler.postprocess(request, response)
        except Exception as e:
            return self._handle_exception(request, e)

    def _handle_exception(self, request, exc):
        status = get_status_from_exc(exc)
        return self._exception_handler(request, exc, status)

    def _start_response(self, response, start_response):
        status = response._get_wsgi_status()
        headers = response._get_wsgi_headers()
        start_response(status, headers)

    __call__ = handle_wsgi_request
