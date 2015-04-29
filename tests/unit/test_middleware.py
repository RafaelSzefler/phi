# -*- coding: utf-8 -*-
import pytest

from phi.middleware import MiddlewareHandler

from tests.dependencies import mock


@pytest.fixture
def mh():
    return MiddlewareHandler()


class TestMiddlewareHandler(object):
    def test__init__(self, mh):
        assert mh._pre_handlers == []
        assert mh._post_handlers == []

    def test_add_pre_handler(self, mh):
        handler1 = mock.Mock()
        handler2 = mock.Mock()
        mh.add_pre_handler(handler1)
        mh.add_pre_handler(handler2)
        assert mh._pre_handlers == [handler1, handler2]

    def test_add_post_handler(self, mh):
        handler1 = mock.Mock()
        handler2 = mock.Mock()
        mh.add_post_handler(handler1)
        mh.add_post_handler(handler2)
        assert mh._post_handlers == [handler1, handler2]

    def test_preprocess(self, mh):
        request = mock.Mock()
        response = mock.Mock()
        handlers = [
            mock.Mock(return_value=None),
            mock.Mock(return_value=response),
            mock.Mock(return_value=None)
        ]
        for handler in handlers:
            mh.add_pre_handler(handler)

        res = mh.preprocess(request)
        assert res == response
        assert handlers[0].called
        assert handlers[1].called
        assert not handlers[2].called

    def test_preprocess_empty(self, mh):
        request = mock.Mock()
        assert mh.preprocess(request) is None

    def test_postprocess(self, mh):
        request = mock.Mock()
        response = mock.Mock()
        new_response = mock.Mock()
        handlers = [
            mock.Mock(return_value=None),
            mock.Mock(return_value=new_response),
            mock.Mock(return_value=None)
        ]
        for handler in handlers:
            mh.add_post_handler(handler)

        res = mh.postprocess(request, response)
        assert res == new_response
        assert handlers[0].called
        assert handlers[1].called
        assert not handlers[2].called

    def test_postprocess_empty(self, mh):
        request = mock.Mock()
        response = mock.Mock()
        assert mh.postprocess(request, response) == response
