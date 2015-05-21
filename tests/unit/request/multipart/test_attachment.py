# -*- coding: utf-8 -*-
from io import BytesIO
import pytest

from phi.request.multipart.attachment import Attachment
from phi.request.multipart.boundary_reader import BoundaryReader
from phi.utils import CaseInsensitiveDict

from tests.dependencies import mock


CONTENT = (
    "Type: test\r\n"
    "Header: xyz  \r\n"
    ": xyz\r\n"
    "\r\n"
    "my superb attachment"
    " with superb content"
)


@pytest.fixture
def br():
    content = CONTENT.encode("utf-8")
    stream = BytesIO(content)
    length = len(content)
    reader = BoundaryReader(
        stream, b"foo", length
    )
    reader.MIN_BUFFER_SIZE = 12
    return reader


@pytest.fixture
def att(br):
    br.initialize(15)
    return Attachment(br, 15)


class TestAttachment(object):
    def test_dry(self, att):
        att.dry()
        assert att._fully_read
        content = list(att.content())
        assert content == []

    def test_bad_headers(self):
        content = b"XYZ"
        stream = BytesIO(content)
        length = len(content)
        reader = BoundaryReader(
            stream, b"foo", length
        )
        reader.MIN_BUFFER_SIZE = 12
        reader.initialize(15)
        att = Attachment(reader, 15)
        with pytest.raises(Exception):
            att.headers

    @mock.patch.object(CaseInsensitiveDict, "__init__", return_value=None)
    def test_headers_caching(self, m_init, att):
        for _ in range(5):
            att.headers
        m_init.assert_called_once_with()

    def test_headers(self, att):
        assert att.headers == {
            b"type": b"test",
            b"header": b"xyz"
        }
