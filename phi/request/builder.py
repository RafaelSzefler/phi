# -*- coding: utf-8 -*-
import re

from six import iteritems

from phi.request.base import BaseRequest
from phi.request.content_request_mapping \
    import CONTENT_TYPE_TO_REQUEST_CLASS_MAP
from phi.request.finite import FiniteRequest
from phi.utils import parse_query_string


HEADER_REGEX = re.compile("^HTTP_")
REPLACE_UNDERSCORES = re.compile("_")

ENV_ATTR_KEYS_MAP = (
    ("url", "PATH_INFO"),
    ("scheme", "wsgi.url_scheme"),
    ("method", "REQUEST_METHOD"),
    ("_content_type", "CONTENT_TYPE"),
    ("content_length", "CONTENT_LENGTH"),
    ("query_string", "QUERY_STRING"),
    ("remote_user", "REMOTE_USER"),
    ("remote_addr", "REMOTE_ADDR"),
    ("_content_stream", "wsgi.input"),
)


class RequestBuilder(object):
    def _build_headers(self, request, env):
        for key, value in iteritems(env):
            if key.startswith("HTTP_"):
                key = HEADER_REGEX.sub("", key)
                key = REPLACE_UNDERSCORES.sub("-", key)
                request.headers[key] = value

    def _build_constant_keys(self, request, env):
        for attr, key in ENV_ATTR_KEYS_MAP:
            value = env.get(key)
            if hasattr(value, "strip"):
                value = value.strip()
            if value not in (None, ""):
                setattr(request, attr, value)
        if request.query_string:
            request.query_params = parse_query_string(request.query_string)
        if request.content_length is not None:
            request.content_length = int(request.content_length)
        request.env = env

    def _get_request_class_from_env(self, env):
        request_class = BaseRequest

        content_length = env.get("CONTENT_LENGTH")
        if content_length in (None, ""):  # We do accept 0 though
            return request_class

        request_class = FiniteRequest

        content_type = env.get("CONTENT_TYPE", "")
        content_type = content_type.partition(";")
        content_type = content_type[0]
        content_type = content_type.strip()

        request_class = CONTENT_TYPE_TO_REQUEST_CLASS_MAP.get(
            content_type, request_class
        )

        return request_class

    def build_request_from_env(self, env):
        request_class = self._get_request_class_from_env(env)
        request = request_class()
        self._build_constant_keys(request, env)
        self._build_headers(request, env)
        return request
