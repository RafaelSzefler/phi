# -*- coding: utf-8 -*-
import pytest

from phi.defaults.decorators import (
    dummy_decorator,
    get_request_object,
    requires_methods
)
from phi.exceptions import HttpMethodNotAllowed
from phi.request.base import BaseRequest

from tests.dependencies import mock


@pytest.fixture
def req():
    return mock.Mock(spec=BaseRequest)


@pytest.fixture
def handler():
    def inner(request):
        return 1
    return inner


def test_dummy_decorator():
    def fn():
        pass

    assert dummy_decorator(fn) is fn


def test_get_request_object(req):
    assert get_request_object([1, None, req, "test"]) is req


def test_get_request_object__exc():
    with pytest.raises(AttributeError):
        get_request_object([1, None, "test"])


def test_requires_methods__dummy(req, handler):
    decorator = requires_methods([])
    assert handler is decorator(handler)


def test_requires_methods__proper(req, handler):
    req.method = "POST"
    decorator = requires_methods(["POST"])
    dhandler = decorator(handler)
    assert dhandler(req) == 1


def test_requires_methods__exc(req, handler):
    req.method = "GET"
    decorator = requires_methods(["POST"])
    dhandler = decorator(handler)
    with pytest.raises(HttpMethodNotAllowed):
        dhandler(req)
