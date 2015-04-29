# -*- coding: utf-8 -*-
from phi.response.file import FileResponse

from tests.dependencies import mock


class TestFileResponsee(object):

    def test_all(self):
        m_open = mock.mock_open(read_data="ala ma kota")
        with mock.patch("phi.response.file.open", m_open, create=True):
            file_res = FileResponse("test.js")

        m_open.assert_called_once_with("test.js", "rb")
        assert file_res.content == "ala ma kota"
        assert file_res.content_type == "application/javascript"
        assert file_res.content_length == 11
