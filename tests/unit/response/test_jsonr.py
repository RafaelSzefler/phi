# -*- coding: utf-8 -*-
import pytest

from phi.response.finite import FiniteResponse
from phi.response.jsonr import JsonResponse


class TestJsonResponse(object):
    @pytest.fixture
    def json_res(self):
        return JsonResponse({"test": 1})

    @pytest.mark.parametrize("base_cls", [FiniteResponse])
    def test_inheritance(self, base_cls, json_res):
        assert isinstance(json_res, base_cls)

    def test_defaults(self, json_res):
        assert json_res.content_type == "application/json"
        assert json_res.status == 200

    @pytest.mark.parametrize("obj, content, content_length", [
        (None, "null", 4),
        ({"test": 1}, '{"test": 1}', 11),
        ([1, 2], "[1, 2]", 6),
        ("test", '"test"', 6),
    ])
    def test_default__init__(self, obj, content, content_length):
        res = JsonResponse(obj)
        assert res.content == content
        assert res.content_length == content_length

    def test_status__init__(self):
        res = JsonResponse(None, status=500)
        assert res.status == 500
