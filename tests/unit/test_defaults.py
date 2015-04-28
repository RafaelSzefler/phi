# -*- coding: utf-8 -*-
from phi.response.http import HttpResponse
from phi.defaults import default_exception_handler


def test_default_exception_handler():
    response = default_exception_handler(None, None, 123)
    assert isinstance(response, HttpResponse)
    assert response.exception is None
    assert response.status == 123


def test_default_exception_handler_exc():
    exc = Exception()
    response = default_exception_handler(None, exc, 123)
    assert isinstance(response, HttpResponse)
    assert response.exception is exc
    assert response.status == 123
