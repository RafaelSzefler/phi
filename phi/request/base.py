# -*- coding: utf-8 -*-
from phi.utils import CaseInsensitiveDict

CACHED_BODY_KEY = "body"
CACHED_CONTENT_KEY = "content"


class BaseRequest(object):
    env = None
    method = None
    url = None
    url_scheme = None
    content_type = None
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
    def body(self):
        raise NotImplementedError

    @property
    def body_iterator(self):
        raise NotImplementedError

    @property
    def content(self):
        raise NotImplementedError
