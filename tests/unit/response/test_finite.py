# -*- coding: utf-8 -*-
import pytest

from phi.response.finite import FiniteResponse

from tests.utils import mock


class TestFiniteResponseMixin(object):

    @pytest.fixture
    def frm(self):
        return FiniteResponse()

    def test__update_header_list_with_content_length(self, frm):
        lst = []
        frm.content_length = 100
        frm._update_header_list_with_content_length(lst)
        assert lst == [
            ("Content-Length", "100")
        ]

    def test__get_wsgi_content_iterator(self, frm):
        frm.content = mock.Mock()
        chunks = list(frm._get_wsgi_content_iterator())
        assert chunks == [frm.content]
