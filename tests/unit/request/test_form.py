# -*- coding: utf-8 -*-
from io import BytesIO

import pytest

from phi.request.form import FormRequest


class TestFormRequest(object):
    @pytest.fixture
    def form_req(self):
        return FormRequest()

    @pytest.mark.parametrize("body, content", [
        (
            "name=test&blah=asdfdasf+&check=on",
            {"blah": "asdfdasf ", "name": "test", "check": "on"}
        ),
        (
            "name=test&blah=asdfdasf+&check=on",
            {"blah": "asdfdasf ", "name": "test", "check": "on"}
        ),
        (
            "name=%C4%85%C5%BA%C5%BA%C4%87+ed+f&blah=",
            {"name": "\xc4\x85\xc5\xba\xc5\xba\xc4\x87 ed f"}
        )
    ])
    def test_body(self, body, content, form_req):
        stream = BytesIO(body)
        stream.seek(0)
        form_req._content_stream = stream
        form_req.content_length = len(body)
        assert form_req._get_body() == content
