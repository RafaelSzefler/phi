# -*- coding: utf-8 -*-
import re
import pytest

from phi.url_routing.pattern import Pattern
from phi.exceptions import ValidationError


@pytest.fixture(scope="module")
def pattern_obj():
    return Pattern(
        regexp_obj=re.compile("^/(?P<xyz>\w+?)/test/(?P<abc>\d+?)/$"),
        groups={
            "xyz": re.compile("^\w+$"),
            "abc": re.compile("^\d+$"),
        }
    )


class TestPattern(object):
    def test__validate_keys_ok(self, pattern_obj):
        pattern_obj._validate_keys({"xyz": 1, "abc": 2})

    @pytest.mark.parametrize("dct", [
        {"xyz": 1},
        {"abc": 2},
        {"test": "foo"},
        {"xyz": 1, "abc": 2, "test": "blah"},
    ])
    def test__validate_keys_exc(self, dct, pattern_obj):
        with pytest.raises(ValidationError):
            pattern_obj._validate_keys(dct)

    @pytest.mark.parametrize("key, value, result", [
        ("xyz", "test", "^/test/test/(?P<abc>\d+?)/$"),
        ("abc", "11", "^/(?P<xyz>\w+?)/test/11/$"),
    ])
    def test__partial_reverse(self, key, value, result, pattern_obj):
        pattern = pattern_obj._regexp_obj.pattern
        assert pattern_obj._partial_reverse(pattern, key, value) == result

    @pytest.mark.parametrize("key, value", [
        ("xyz", " %$@"),
        ("abc", "test"),
    ])
    def test__partial_reverse_exc(self, key, value, pattern_obj):
        with pytest.raises(ValidationError):
            pattern_obj._partial_reverse("", key, value)

    def test_reverse(self, pattern_obj):
        assert pattern_obj.reverse(xyz="foo", abc=11) == "/foo/test/11/"

    @pytest.mark.parametrize("url, matched, params", [
        ("/foo/test/11/", True, {"xyz": "foo", "abc": "11"}),
        ("/blah/test/666/", True, {"xyz": "blah", "abc": "666"}),
        ("/xyz", False, None),
    ])
    def test_match(self, url, matched, params, pattern_obj):
        assert pattern_obj.match(url) == (matched, params)
