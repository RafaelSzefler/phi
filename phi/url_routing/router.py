# -*- coding: utf-8 -*-
from phi.exceptions import RoutingException, HttpNotFound
from phi.url_routing.pattern_builder import PatternBuilder


class URLRouter(object):

    def __init__(self, pattern_builder_factory=PatternBuilder):
        self._handlers = {}
        self._patterns = []
        self._patter_builder = pattern_builder_factory()

    def add_route(self, name, pattern, handler):
        if name in self._handlers:
            raise RoutingException(
                "Route [{name}] already exists!".format(name=name)
            )
        pattern_obj = self._patter_builder.from_simple_pattern(pattern)
        route = (name, pattern_obj, handler)
        self._handlers[name] = route
        self._patterns.append(route)

    def reverse(self, name, params={}):
        if name not in self._handlers:
            raise KeyError("Pattern [{name}] not defined!".format(name=name))
        pattern = self._handlers[name][1]
        return pattern.reverse(params)

    def get_handler_and_params_from_url(self, url):
        for _, pattern, handler in self._patterns:
            matched, params = pattern.match(url)
            if matched:
                return handler, params
        raise HttpNotFound

    def get_handler_and_params_from_request(self, request):
        return self.get_handler_and_params_from_url(request.url)
