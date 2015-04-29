# -*- coding: utf-8 -*-
import re

from io import BytesIO

from six import iteritems
from six.moves.urllib.parse import urlencode

UNDERSCORE_RE = re.compile("-")


class TestApplication(object):
    _user_agent = "phi/testing"

    def __init__(self, application):
        self._application = application

    def request(
        self, url, content_type="text/plain", method="GET", body=None,
        headers={}, query_params={}, charset="utf-8"
    ):
        env = self._build_env(
            url=url,
            content_type=content_type,
            method=method,
            body=body,
            headers=headers,
            query_params=query_params,
            charset=charset
        )
        return self._make_request(env)

    def _make_request(self, env):
        response = {}

        def start_response(status, headers):
            response["status"] = status
            response["headers"] = dict(headers)

        body = self._application.handle_wsgi(env, start_response)
        body = list(body)
        body = "".join(body)
        response["body"] = body
        return response

    def _build_env(
        self, url, content_type, method, body, headers, query_params, charset
    ):
        stream = BytesIO()
        content_length = 0
        if body is not None:
            body = body.encode(charset)
            content_length = len(body)
            stream.write(body)
            stream.seek(0)

        env = {
            "wsgi.input": stream,
            "PATH_INFO": url,
            "REQUEST_METHOD": method,
            "CONTENT_TYPE": content_type,
            "CONTENT_LENGTH": str(content_length),
            "QUERY_STRING": urlencode(query_params)
        }

        self._update_headers(env, headers)

        return env

    def _update_headers(self, env, headers):
        env["HTTP_USER_AGENT"] = self._user_agent
        for key, value in iteritems(headers):
            header = UNDERSCORE_RE.sub("_", key)
            header = header.upper()
            header = "HTTP_" + header
            env[header] = str(value)
