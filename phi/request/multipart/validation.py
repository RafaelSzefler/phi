# -*- coding: utf-8 -*-
import re

from phi.exceptions import ValidationError

BOUNDARY_VALID = re.compile("^[0-9a-zA-Z'()+_,-./:=? ]*$")


def validate_multipart_boundary_value(value):
    if not value:
        raise ValidationError("Content-Type: passed empty boundary")

    if len(value) > 70:
        raise ValidationError("Content-Type: boundary too long")

    if not BOUNDARY_VALID.search(value):
        raise ValidationError("Content-Type: boundary not HTTP compliant")

    return True
