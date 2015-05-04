# -*- coding: utf-8 -*-
import re
import traceback
from os import path

from phi.constants import STATUSES, UNKNOWN_STATUS
from phi.response.http import HttpResponse
from phi.response.file import FileResponse


CONTENT = """
<!DOCTYPE html>
<head></head>
<body>
    <div><strong>{error}</strong></div>
    <div><pre>{traceback}</pre></div>
</body>
"""


def default_exception_handler(request, exc, status):
    code = STATUSES.get(status, UNKNOWN_STATUS)
    tr = "" if exc is None else traceback.format_exc()
    content = CONTENT.format(
        error="{status} {code}".format(status=status, code=code),
        traceback=tr,
    )
    response = HttpResponse(content, status=status)
    if exc is not None:
        response.exception = exc
    return response


class StaticsHandler(object):
    def __init__(self, prefix, root_folder=""):
        self._prefix = prefix
        pattern = "^" + re.escape(prefix)
        self._prefix_re = re.compile(pattern)
        self._root_folder = root_folder

    def _is_static_request(self, request):
        return request.url.startswith(self._prefix)

    def _get_path_from_request(self, request):
        url = request.url
        file_path = self._prefix_re.sub("", url)
        path_components = file_path.split("/")
        full_path = path.join(self._root_folder, *path_components)
        return full_path

    def _get_response(self, file_path):
        if not path.exists(file_path):
            return HttpResponse("", content_type="text/plain", status=404)
        return FileResponse(file_path)

    def __call__(self, request):
        if not self._is_static_request(request):
            return

        file_path = self._get_path_from_request(request)
        return self._get_response(file_path)
