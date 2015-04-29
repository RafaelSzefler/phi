# -*- coding: utf-8 -*-
import pytest

# We do that renaming so that py.test won't try to interpret
# TestApplication as a test case.
from phi.testing.core import TestApplication as CTestApplication

from tests.dependencies import mock


@pytest.fixture(scope="module")
def tapp(app):
    return CTestApplication(app)


@pytest.fixture
def tparams():
    return {
        "url": mock.Mock(),
        "content_type": mock.Mock(),
        "method": mock.Mock(),
        "body": mock.Mock(),
        "headers": mock.Mock(),
        "query_params": mock.Mock(),
        "charset": mock.Mock()
    }


class TestTestApplication(object):

    def test___init__(self, tapp, app):
        assert tapp._application is app

    @mock.patch.object(CTestApplication, "_build_env")
    @mock.patch.object(CTestApplication, "_make_request")
    def test_request(self, m_make, m_build, tapp, tparams):
        resp = tapp.request(**tparams)
        m_build.assert_called_once_with(**tparams)
        env = m_build(**tparams)
        m_make.assert_called_once_with(env)
        assert resp == m_make(env)

    def test__make_request(self, request, tapp):
        _app = tapp._application

        def revert():
            tapp._application = _app

        request.addfinalizer(revert)

        my_env = mock.Mock(spec=dict)
        app = mock.Mock(spec=CTestApplication)
        tapp._application = app

        def new_handle_wsgi(env, start):
            assert env is my_env
            start(
                "test status",
                [("my-header", "foo"), ("my-other-header", "baz")]
            )
            return ["test1", "test2"]

        app.handle_wsgi_request.side_effect = new_handle_wsgi
        response = tapp._make_request(my_env)
        assert response == {
            "body": "test1test2",
            "headers": {
                "my-header": "foo",
                "my-other-header": "baz"
            },
            "status": "test status"
        }

    def test__build_env(self, tapp):
        env = tapp._build_env(
            url="/test",
            content_type="foo/bar",
            method="XYZ",
            body="ala ma kota",
            headers={"my-header": 11},
            query_params={"my-query": "ugh"},
            charset="utf-8"
        )
        stream = env["wsgi.input"]
        assert env == {
            "CONTENT_LENGTH": "11",
            "CONTENT_TYPE": "foo/bar",
            "HTTP_MY_HEADER": "11",
            "HTTP_USER_AGENT": "phi/testing",
            "PATH_INFO": "/test",
            "QUERY_STRING": "my-query=ugh",
            "REQUEST_METHOD": "XYZ",
            "wsgi.input": stream
        }
        assert stream.read() == b"ala ma kota"

    def test__build_env_no_body(self, tapp):
        env = tapp._build_env(
            url="/test",
            content_type="foo/bar",
            method="XYZ",
            body=None,
            headers={"my-header": 11},
            query_params={"my-query": "ugh"},
            charset="utf-8"
        )
        stream = env["wsgi.input"]
        assert env == {
            "CONTENT_LENGTH": "0",
            "CONTENT_TYPE": "foo/bar",
            "HTTP_MY_HEADER": "11",
            "HTTP_USER_AGENT": "phi/testing",
            "PATH_INFO": "/test",
            "QUERY_STRING": "my-query=ugh",
            "REQUEST_METHOD": "XYZ",
            "wsgi.input": stream
        }
        assert stream.read() == b""

    def test__update_headers(self, tapp):
        env = {}
        headers = {"test": 1, "foo-xyz": "bar"}
        tapp._update_headers(env, headers)
        assert env == {
            "HTTP_USER_AGENT": "phi/testing",
            "HTTP_TEST": "1",
            "HTTP_FOO_XYZ": "bar"
        }
