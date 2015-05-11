# -*- coding: utf-8 -*-
from datetime import datetime

import six

from phi.constants import STATUSES, UNKNOWN_STATUS
from phi.utils import (
    CaseInsensitiveDict,
    capitalize_first_letters_in_sentence
)


class CookieDict(dict):
    def set_cookie(
        self, key, value, path=None, domain=None, max_age=None,
        secure=False, http_only=False, expires=None
    ):
        cookie = [str(value)]
        if path:
            cookie.append("Path={}".format(path))

        if domain:
            cookie.append("Domain={}".format(domain))

        if max_age:
            cookie.append("Max-Age={}".format(max_age))

        if expires:
            expires = expires.strftime("%a, %d-%b-%Y %T GMT")
            cookie.append("Expires={}".format(expires))

        if secure:
            cookie.append("Secure")

        if http_only:
            cookie.append("HttpOnly")

        cookie = ";".join(cookie)
        self[key] = cookie

    def expire_cookie(self, key):
        self.set_cookie(key, "", expires=datetime(2015, 1, 1))


class BaseResponse(object):
    status = 200
    content = None
    charset = "utf-8"
    content_type = "text/plain"
    content_length = None
    exception = None

    def __init__(self):
        self.headers = CaseInsensitiveDict()
        self.cookies = CookieDict()

    @property
    def status_reason(self):
        return STATUSES.get(self.status, UNKNOWN_STATUS)

    def _get_wsgi_status(self):
        return "{status} {reason}".format(
            status=self.status,
            reason=self.status_reason
        )

    def _update_header_list_with_content_length(self, header_list):
        raise NotImplementedError

    def _get_full_content_type(self):
        return "{content_type}; charset={charset}".format(
            content_type=self.content_type,
            charset=self.charset
        )

    def _update_header_list_with_headers(self, header_list):
        content_type = self._get_full_content_type()
        header_list.append(("Content-Type", content_type))
        for header, value in six.iteritems(self.headers):
            header = capitalize_first_letters_in_sentence(header)
            value = str(value)
            header_list.append((header, value))

    def _update_cookies(self, wsgi_headers):
        for key, value in six.iteritems(self.cookies):
            wsgi_headers.append(
                (
                    "Set-Cookie",
                    "{key}={value}".format(
                        key=key,
                        value=value
                    )
                )
            )

    def _get_wsgi_headers(self):
        wsgi_headers = []
        self._update_header_list_with_headers(wsgi_headers)
        self._update_header_list_with_content_length(wsgi_headers)
        self._update_cookies(wsgi_headers)
        return wsgi_headers

    def _get_wsgi_content_iterator(self):
        raise NotImplementedError
