# -*- coding: utf-8 -*-
import pytest

from phi import Application, URLRouter


@pytest.fixture(scope="module")
def url_router():
    return URLRouter()


@pytest.fixture(scope="module")
def app(url_router):
    app = Application()
    app._url_router = url_router
    return app
