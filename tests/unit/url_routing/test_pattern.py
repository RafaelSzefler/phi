# -*- coding: utf-8 -*-
import re
import pytest

from phi.url_routing.pattern import Pattern, PatternBuilder
from phi.exceptions import ValidationError

from tests.dependencies import mock


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


@pytest.fixture(scope="module")
def pb():
    return PatternBuilder()


class TestPatternBuilder(object):
    @pytest.mark.parametrize("group, group_dict, pattern", [
        ("{test}", {"test": re.compile("^\w+$")}, "(?P<test>\w+?)"),
        ("{xyz:\d+}", {"xyz": re.compile("^\d+$")}, "(?P<xyz>\d+?)"),
    ])
    def test__handle_group_case(self, group, group_dict, pattern, pb):
        named_groups = {}
        full_pattern = []
        pb._handle_group_case(group, full_pattern, named_groups)
        assert full_pattern == [pattern]
        assert set(named_groups) == set(group_dict)
        keys = list(named_groups.keys())
        assert len(keys) == 1
        key = keys[0]
        named_r = named_groups[key]
        gr_r = group_dict[key]
        assert named_r.pattern == gr_r.pattern

    @mock.patch.object(PatternBuilder, "_handle_group_case")
    def test__process_groups(self, m_handle, pb):
        full_pattern = []
        named_groups = {}
        groups = ["test", "foo", "bar", "baz", "xyz"]
        pb._process_groups(groups, full_pattern, named_groups)
        assert full_pattern == ["test", "bar", "xyz"]
        assert m_handle.call_args_list == [
            mock.call("foo", full_pattern, named_groups),
            mock.call("baz", full_pattern, named_groups),
        ]

    @pytest.mark.parametrize("groups, result", [
        (["test"], "^test$"),
        (["xyz", "blah"], "^xyzblah$"),
        (["test", "(?P<id>\w+)"], "^test(?P<id>\w+)$"),
    ])
    def test__build_regexp(self, groups, result, pb):
        regexp = pb._build_regexp(groups)
        assert regexp.pattern == result

    @pytest.mark.parametrize("pattern, regexp", [
        ("/test", "^/test$"),
        ("/test{xyz}", "^/test(?P<xyz>\w+?)$"),
        ("/{xyz}/test/{abc:\d+}/", "^/(?P<xyz>\w+?)/test/(?P<abc>\d+?)/$"),
    ])
    def test_from_simple_pattern(self, pattern, regexp, pb):
        pattern_obj = pb.from_simple_pattern(pattern)
        assert isinstance(pattern_obj, Pattern)
        assert pattern_obj._regexp_obj.pattern == regexp
