# -*- coding: utf-8 -*-
import pytest

from phi.utils import (
    CaseInsensitiveDict,
    capitalize_first_letter,
    capitalize_first_letters_in_sentence,
    get_status_from_exc,
    parse_query_string
)
from phi.exceptions import (
    HttpException,
    HttpNotFound,
    HttpForbidden,
    HttpBadRequest
)

from tests.dependencies import mock


@pytest.fixture
def cid():
    cid = CaseInsensitiveDict()
    cid["Test"] = 1
    cid["foo"] = 2
    cid["blah"] = 3
    cid["BLAH"] = 4
    cid["fOO"] = 5
    return cid


class TestUtils(object):
    @pytest.mark.parametrize("src, result", [
        ("", ""),
        ("a", "A"),
        ("B", "B"),
        ("test", "Test"),
        ("TEST", "TEST"),
        ("fOO", "FOO"),
        ("bAr", "BAr"),
        ("Baa", "Baa"),
        ("BaR", "BaR")
    ])
    def test_capitalize_first_letter(self, src, result):
        assert capitalize_first_letter(src) == result

    @pytest.mark.parametrize("src, result", [
        ("test", "Test"),
        ("Foo", "Foo"),
        ("ala ma kota", "Ala Ma Kota"),
        ("Ala ma-kota I co?", "Ala Ma-Kota I Co?"),
        ("   test IT---", "   Test IT---")
    ])
    def test_capitalize_first_letters_in_sentence(self, src, result):
        assert capitalize_first_letters_in_sentence(src) == result

    @pytest.mark.parametrize("exc, result", [
        (Exception, 500),
        (KeyError, 500),
        (HttpException, 500),
        (HttpBadRequest, 400),
        (HttpForbidden, 403),
        (HttpNotFound, 404),
    ])
    def test_get_status_from_exc(self, exc, result):
        assert get_status_from_exc(exc) == result

    @pytest.mark.parametrize("qs, data", [
        ("test=1", {"test": "1"}),
        (
            "name=%C4%85%C5%BA%C5%BA%C4%87+ed+f&blah=",
            {"name": "\xc4\x85\xc5\xba\xc5\xba\xc4\x87 ed f"}
        ),
        (
            "test=1&foo=2&test=3",
            {"test": ["1", "3"], "foo": "2"}
        ),
        ("foo=ala+ma++kota", {"foo": "ala ma  kota"})
    ])
    def test_parse_query_string(self, qs, data):
        assert parse_query_string(qs) == data


class TestCaseInsensitiveDict(object):
    @pytest.mark.parametrize("key, value", [
        ("test", 1),
        ("Foo", 5),
        ("bLAh", 4),
    ])
    def test_get_item(self, cid, key, value):
        assert cid[key] == value

    def test_set_item(self, cid):
        value = mock.Mock()
        cid["XYZ"] = value
        assert cid["xyz"] is value
        assert cid["xYz"] is value

    def test_del_item(self, cid):
        del cid["test"]
        del cid["foo"]
        del cid["BLah"]
        assert not cid

    @pytest.mark.parametrize("key", [
        "test", "FoO", "bLAh"
    ])
    def test_contains(self, cid, key):
        assert key in cid

    @pytest.mark.parametrize("key, default, result", [
        ("test", 6, 1),
        ("xyz", "test", "test"),
        ("foo", None, 5),
    ])
    def test_get(self, cid, key, default, result):
        assert cid.get(key, default) == result

    def test_pop(self, cid):
        value = cid.pop("blah")
        assert value == 4
        assert "blah" not in cid
