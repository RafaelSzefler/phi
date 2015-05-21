# -*- coding: utf-8 -*-
import pytest

from phi.exceptions import ValidationError
from phi.request.multipart.validation import validate_multipart_boundary_value


class TestMultipartBoundaryValidator(object):

    @pytest.mark.parametrize("boundary", [
        "alfa", "test xyz", "0az", "0a23BCd34_'(xyz),-.//xyz=??", "xyz:132 i 1"
    ])
    def test_correct_multipart(self, boundary):
        assert validate_multipart_boundary_value(boundary)

    @pytest.mark.parametrize("boundary", [
        "", "a"*71, "a!@#$", "test \"", "[xyz]"
    ])
    def test_wrong_multipart(self, boundary):
        with pytest.raises(ValidationError):
            validate_multipart_boundary_value(boundary)
