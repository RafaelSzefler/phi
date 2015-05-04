# -*- coding: utf-8 -*-
import re

import six

from phi.exceptions import ValidationError


class Pattern(object):
    def __init__(self, regexp_obj=None, groups={}):
        self._regexp_obj = regexp_obj
        self._groups = groups
        self._group_keys = set(groups)

    def _validate_keys(self, params):
        param_keys = set(params)
        if param_keys != self._group_keys:
            raise ValidationError(
                "Passed params incompatible with the pattern."
            )

    def _partial_reverse(self, pattern, key, value):
        value = str(value)
        validate = self._groups[key]
        if not validate.match(value):
            raise ValidationError(
                "[{value}] value for [{key}] key "
                "does not match [{regexp}] regexp.".format(
                    key=key,
                    value=value,
                    regexp=validate.pattern
                )
            )

        regexp_obj = re.compile("\(\?P<{key}>(.*?)\)".format(key=key))
        return regexp_obj.sub(str(value), pattern)

    def reverse(self, **params):
        self._validate_keys(params)
        pattern = self._regexp_obj.pattern
        for key, value in six.iteritems(params):
            pattern = self._partial_reverse(pattern, key, value)
        return pattern.lstrip("^").rstrip("$")

    def match(self, url):
        match_obj = self._regexp_obj.search(url)
        if not match_obj:
            return False, None
        return True, match_obj.groupdict()
