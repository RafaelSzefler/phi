# -*- coding: utf-8 -*-
import traceback

from phi.constants import STATUSES, UNKNOWN_STATUS
from phi.response.http import HttpResponse


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
