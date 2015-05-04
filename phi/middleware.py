# -*- coding: utf-8 -*-


class Middleware(object):
    def __init__(self):
        self._pre_handlers = []
        self._post_handlers = []

    def add_pre_handler(self, handler):
        self._pre_handlers.append(handler)

    def add_post_handler(self, handler):
        self._post_handlers.append(handler)

    def preprocess(self, request):
        for handler in self._pre_handlers:
            response = handler(request)
            if response is not None:
                return response

    def postprocess(self, request, response):
        for handler in self._post_handlers:
            res = handler(request, response)
            if res is not None:
                return res
            response = res
        return response
