# -*- coding: utf-8 -*-
import pytest

from phi.response.finite import FiniteResponse
from phi.response.msgpackr import MsgpackResponse

from tests.dependencies import mock


class TestMsgpackResponse(object):
    @pytest.fixture
    def msgpack_res(self):
        return MsgpackResponse({"test": 1})

    @mock.patch('phi.response.msgpackr.msgpack', new=None)
    def test_no_msgpack(self):
        with pytest.raises(ImportError):
            MsgpackResponse('test')

    @pytest.mark.parametrize("base_cls", [FiniteResponse])
    def test_inheritance(self, base_cls, msgpack_res):
        assert isinstance(msgpack_res, base_cls)

    def test_defaults(self, msgpack_res):
        assert msgpack_res.content_type == "application/msgpack"
        assert msgpack_res.status == 200

    @pytest.mark.parametrize("obj, content, content_length", [
        (None, b"\xc0", 1),
        ({"test": 1}, b"\x81\xa4test\x01", 7),
        ([1, 2], b"\x92\x01\x02", 3),
        ("test", b"\xa4test", 5),
    ])
    def test_default__init__(self, obj, content, content_length):
        res = MsgpackResponse(obj)
        assert res.content == content
        assert res.content_length == content_length

    def test_status__init__(self):
        res = MsgpackResponse(None, status=500)
        assert res.status == 500
