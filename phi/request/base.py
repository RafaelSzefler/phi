# -*- coding: utf-8 -*-
from phi.utils import CaseInsensitiveDict

CACHED_BODY_KEY = "body"
CACHED_CONTENT_KEY = "content"
CACHED_CONTENT_TYPE_KEY = "content_type"


class BaseRequest(object):
    env = None
    method = None
    url = None
    scheme = None
    _content_type = None
    content_length = None
    charset = "utf-8"
    query_string = None
    remote_user = None
    remote_addr = None
    _content_stream = None

    def __init__(self):
        self.headers = CaseInsensitiveDict()
        self.query_params = {}
        self._cache = {}

    @property
    def content_type(self):
        if CACHED_CONTENT_TYPE_KEY not in self._cache:
            content = self._content_type
            content = content.partition(";")
            content = content[0]
            content = content.strip()
            self._cache[CACHED_CONTENT_TYPE_KEY] = content
        return self._cache[CACHED_CONTENT_TYPE_KEY]

    @property
    def body(self):
        if CACHED_BODY_KEY not in self._cache:
            self._cache[CACHED_BODY_KEY] = self._get_body()
        return self._cache[CACHED_BODY_KEY]

    def _get_body(self):
        raise NotImplementedError

    @property
    def content(self):
        if CACHED_CONTENT_KEY not in self._cache:
            self._cache[CACHED_CONTENT_KEY] = self._get_content()
        return self._cache[CACHED_CONTENT_KEY]

    def _get_content(self):
        raise NotImplementedError

    def content_iterator(self):
        raise NotImplementedError

    def is_ajax(self):
        header = self.headers.get("X-Requested-With")
        if hasattr(header, "lower"):
            header = header.lower()
        return header == "xmlhttprequest"
