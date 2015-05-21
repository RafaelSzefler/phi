# -*- coding: utf-8 -*-
from io import BytesIO

import pytest

from phi.exceptions import ValidationError
from phi.request.multipart.multipart_request import MultipartRequest
from phi.request.multipart.boundary_reader import BoundaryReader

from tests.dependencies import mock


CONTENT = (
    "preamble"
    "\r\n--foo\r\n"
    "Type: test\r\n"
    "Header: xyz\r\n"
    "\r\n"
    "first attachment"
    "\r\n--foo\r\n"
    "\r\n"
    "second attachment"
    "\r\n--foo\r\n"
    "\r\n"
    "third attachment"
    "\r\n--foo\r\n"
    "X: Z\r\n"
    "\r\n"
    "fourth attachment"
    "\r\n--foo--\r\n"
    "epilogue"
)


@pytest.fixture
def req():
    request = MultipartRequest()
    request._content_type = b"multipart/form-data; boundary=foo"
    content = CONTENT.encode("utf-8")
    request._content_stream = BytesIO(content)
    request.content_length = len(content)
    return request


class TestMultipartRequest(object):
    @pytest.mark.parametrize("content_type", [
        b"multipart/form-data",
        b"multipart/form-data;",
        b"multipart/form-data; blah=1",
    ])
    def test__get_boundary_value__exc(self, content_type, req):
        req._content_type = content_type
        with pytest.raises(ValidationError):
            req._get_boundary_value()

    def test__get_boundary_value(self, req):
        assert req._get_boundary_value() == b"foo"

    def test_attachments(self, req):
        attachments = list(req.attachments())
        assert len(attachments) == 4

    def test_attachments_content_big_buffer(self, req):
        attachments = req.attachments()

        first_attachment = next(attachments)
        assert first_attachment.headers == {
            b"type": b"test",
            b"header": b"xyz"
        }

        content = list(first_attachment.content())
        assert content == [b"first attachment"]

        second_attachment = next(attachments)
        assert second_attachment.headers == {}
        content = list(second_attachment.content())
        assert content == [b"second attachment"]

        third_attachment = next(attachments)
        assert third_attachment.headers == {}
        content = list(third_attachment.content())
        assert content == [b"third attachment"]

        fourth_attachment = next(attachments)
        assert fourth_attachment.headers == {b"x": b"Z"}
        content = list(fourth_attachment.content())
        assert content == [b"fourth attachment"]

    @mock.patch.object(BoundaryReader, "MIN_BUFFER_SIZE", new=12)
    def test_attachments_content_small_buffer(self, req):
        req.READ_BUFFER = 12
        attachments = req.attachments()

        first_attachment = next(attachments)
        content = list(first_attachment.content())
        assert content == [b"firs", b"t attachment"]

        second_attachment = next(attachments)
        content = list(second_attachment.content())
        assert content == [b"s", b"econd attach", b"ment"]

        third_attachment = next(attachments)
        content = list(third_attachment.content())
        assert content == [b"third att", b"achment"]
