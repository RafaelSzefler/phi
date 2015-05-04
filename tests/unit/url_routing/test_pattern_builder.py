# -*- coding: utf-8 -*-
import re
import pytest

from phi.url_routing.pattern import Pattern
from phi.url_routing.pattern_builder import PatternBuilder

from tests.dependencies import mock


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
