# -*- coding: utf-8 -*-
import re
from os import path

import pytest

from phi.defaults.statics import StaticsHandler
from phi.request.base import BaseRequest
from phi.response.http import HttpResponse
from phi.response.file import FileResponse

from tests.dependencies import mock


class TestStaticsHandler(object):
    @pytest.fixture
    def static_handler(self):
        return StaticsHandler("/statics/", "foo")

    def test___init__(self, static_handler):
        assert static_handler._prefix == "/statics/"
        assert static_handler._prefix_re == re.compile("^\/statics\/")
        assert static_handler._root_folder == "foo"

    @pytest.mark.parametrize("url, result", [
        ("/static/xyz", False),
        ("/statics/test.js", True),
        ("/statics/xyz/", False),
    ])
    def test___is_static_request(self, static_handler, url, result):
        request = mock.Mock(spec=BaseRequest)
        request.url = url
        assert static_handler._is_static_request(request) is result

    @pytest.mark.parametrize("url, file_path", [
        ("/statics/xyz.js", path.join("foo", "xyz.js")),
        ("/statics/test/blah.xyz", path.join("foo", "test", "blah.xyz")),
    ])
    def test__get_path_from_request(self, static_handler, url, file_path):
        request = mock.Mock(spec=BaseRequest)
        request.url = url
        assert static_handler._get_path_from_request(request) == file_path

    @mock.patch.object(path, "exists", return_value=True)
    @mock.patch.object(FileResponse, "__init__", return_value=None)
    def test__get_response_exists(self, m_init, m_exists, static_handler):
        response = static_handler._get_response("test")
        m_exists.assert_called_once_with("test")
        m_init.assert_called_once_with("test")
        assert isinstance(response, FileResponse)

    @mock.patch.object(path, "exists", return_value=False)
    def test__get_response_not_exists(self, m_exists, static_handler):
        response = static_handler._get_response("test")
        m_exists.assert_called_once_with("test")
        assert isinstance(response, HttpResponse)
        assert response.status == 404

    @mock.patch.object(StaticsHandler, "_is_static_request", return_value=True)
    @mock.patch.object(StaticsHandler, "_get_path_from_request")
    @mock.patch.object(StaticsHandler, "_get_response")
    def test___call__(self, m_resp, m_path, m_is, static_handler):
        request = mock.Mock(spec=BaseRequest)
        response = static_handler(request)
        m_is.assert_called_once_with(request)
        m_path.assert_called_once_with(request)
        file_path = m_path(request)
        m_resp.assert_called_once_with(file_path)
        assert response == m_resp(file_path)

    @mock.patch.object(
        StaticsHandler, "_is_static_request", return_value=False)
    @mock.patch.object(StaticsHandler, "_get_path_from_request")
    @mock.patch.object(StaticsHandler, "_get_response")
    def test___call___wrong_url(self, m_resp, m_path, m_is, static_handler):
        request = mock.Mock(spec=BaseRequest)
        response = static_handler(request)
        m_is.assert_called_once_with(request)
        assert not m_path.called
        assert not m_resp.called
        assert response is None
