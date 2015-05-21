# -*- coding: utf-8 -*-
from phi.exceptions import ValidationError
from phi.request.base import BaseRequest
from phi.request.multipart.attachment import Attachment
from phi.request.multipart.boundary_reader import BoundaryReader, dry_generator
from phi.request.multipart.validation import validate_multipart_boundary_value

BOUNDARY = b"boundary="
BOUNDARY_LEN = len(BOUNDARY)


class MultipartRequest(BaseRequest):
    READ_BUFFER = 2**12

    def _get_boundary_value(self):
        full_content_type = self._content_type.partition(b";")
        boundary = full_content_type[2]
        if not boundary:
            raise ValidationError(
                "Content-Type: no boundary"
            )

        boundary = boundary.strip()
        if not boundary.startswith(BOUNDARY):
            raise ValidationError(
                "Content-Type: boundary has to start with 'boundary=' prefix"
            )

        boundary_value = boundary[BOUNDARY_LEN:]
        return boundary_value.strip(b'"').rstrip()

    def attachments(self):
        boundary = self._get_boundary_value()
        validate_multipart_boundary_value(boundary.decode("utf-8"))

        boundary_reader = BoundaryReader(
            self._content_stream, boundary, self.content_length
        )
        boundary_reader.initialize()

        # Content before first boundary has to be omitted (RFC1341)
        generator = boundary_reader.read_until_next_boundary(
            self.READ_BUFFER
        )
        dry_generator(generator)

        while not boundary_reader.is_dry():
            attachment = Attachment(boundary_reader, self.READ_BUFFER)
            yield attachment
            if not attachment.fully_read():
                attachment.dry()
