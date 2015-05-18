# -*- coding: utf-8 -*-
import pytest

from phi.defaults.action_controller import ActionController
from phi.exceptions import HttpNotFound
from phi.request.base import BaseRequest

from tests.dependencies import mock


class MyController(ActionController):
    BAZ = 5

    def home(self, request):
        return 1

    def foo(self):
        return 2

    def bar(self, request, xyz):
        return (3, xyz)

    def _test(self, request):
        return 4


@pytest.fixture
def controller():
    return MyController()


@pytest.fixture
def req():
    return mock.Mock(spec=BaseRequest)


class TestActionController(object):
    @pytest.mark.parametrize("action", [
        "_foo", None, "xyz", 0, "BAZ"
    ])
    def test___call___wrong(self, action, controller, req):
        with pytest.raises(HttpNotFound):
            controller(req, action=action)

    def test___call___no_request(self, controller, req):
        with pytest.raises(TypeError):
            controller(req, action="foo")

    def test___call___kwarg(self, controller, req):
        xyz = mock.Mock()
        result = controller(req, action="bar", xyz=xyz)
        assert result == (3, xyz)

    def test___call__(self, controller, req):
        result = controller(req, action="home")
        assert result == 1

    def test___init__(self):
        controller = MyController("blah")
        assert controller._action_name == "blah"
