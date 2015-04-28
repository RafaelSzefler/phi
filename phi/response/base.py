# -*- coding: utf-8 -*-
import six

from phi.constants import STATUSES, UNKNOWN_STATUS
from phi.utils import (
    CaseInsensitiveDict,
    capitalize_first_letters_in_sentence
)


class FiniteResponseMixin(object):
    def _update_header_list_with_content_length(self, header_list):
        header_list.append(("Content-Length", str(self.content_length)))

    def _get_wsgi_content_iterator(self):
        yield self.content


class BaseResponse(object):
    status = 200
    content = None
    charset = "utf-8"
    content_type = "text/plain"
    content_length = None
    exception = None

    def __init__(self):
        self.headers = CaseInsensitiveDict()

    def _get_wsgi_status(self):
        status = self.status
        status_name = STATUSES.get(status, UNKNOWN_STATUS)
        return "{status} {status_name}".format(
            status=status,
            status_name=status_name
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

    def _get_wsgi_headers(self):
        wsgi_headers = []
        self._update_header_list_with_headers(wsgi_headers)
        self._update_header_list_with_content_length(wsgi_headers)
        return wsgi_headers

    def _get_wsgi_content_iterator(self):
        raise NotImplementedError
