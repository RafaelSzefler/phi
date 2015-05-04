# -*- coding: utf-8 -*-
import re

from phi.url_routing.pattern import Pattern

GROUPS_RE = re.compile("(\{.*?\})")
REMOVE_RE = re.compile("(^\{*)|(\}*$)")


class PatternBuilder(object):
    def _handle_group_case(self, group, full_pattern, named_groups):
        stripped = REMOVE_RE.sub("", group)
        label, _, regexp = stripped.partition(":")
        regexp = regexp or "\\w+"
        named_groups[label] = re.compile("^"+regexp+"$")
        full_regexp = "(?P<{label}>{regex}?)".format(
            label=label,
            regex=regexp
        )
        full_pattern.append(full_regexp)

    def _process_groups(self, groups, full_pattern, named_groups):
        for i, group in enumerate(groups):
            if i % 2 == 0:
                full_pattern.append(group)
            else:
                self._handle_group_case(group, full_pattern, named_groups)

    def _build_regexp(self, full_pattern):
        pattern = "".join(full_pattern)
        regexp = "^{pattern}$".format(pattern=pattern)
        return re.compile(regexp)

    def from_simple_pattern(self, pattern):
        full_pattern = []
        named_groups = {}
        groups = GROUPS_RE.split(pattern)
        self._process_groups(groups, full_pattern, named_groups)
        regexp_obj = self._build_regexp(full_pattern)
        return Pattern(
            regexp_obj=regexp_obj,
            groups=named_groups
        )
