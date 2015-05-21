# -*- coding: utf-8 -*-
from phi.request.multipart.boundary_reader import CRLF, dry_generator
from phi.utils import CaseInsensitiveDict

DOUBLE_CRLF = CRLF+CRLF


class Attachment(object):
    def __init__(self, boundary_reader, buffer_size):
        self._fully_read = False
        self._headers_read = False
        self._leftover = None
        self._generator = boundary_reader.read_until_next_boundary(
            buffer_size
        )

    def dry(self):
        dry_generator(self._generator)
        self._fully_read = True

    def fully_read(self):
        return self._fully_read

    def _build_headers(self, headers_list):
        headers = b"".join(headers_list)
        headers = headers.split(CRLF)
        for header in headers:
            key, _, value = header.partition(b":")
            key = key.strip()
            if not key:
                continue
            value = value.strip()
            self._headers[key] = value

    def _read_headers(self):
        if self._headers_read:
            return

        self._headers = CaseInsensitiveDict()
        self._headers_read = True

        first_chunk = next(self._generator)
        if first_chunk.startswith(CRLF):
            self._leftover = first_chunk[len(CRLF):]
            return

        headers = []
        current_chunk = first_chunk
        for next_chunk in self._generator:
            extended_chunk = current_chunk + next_chunk

            before, separator, after = extended_chunk.partition(DOUBLE_CRLF)

            if separator:
                headers.append(before)
                self._leftover = after
                break

            headers.append(current_chunk)
            current_chunk = next_chunk

        if not headers:
            before, separator, after = first_chunk.partition(DOUBLE_CRLF)
            if not separator:
                raise Exception("Headers not found!")
            headers.append(before)
            self._leftover = after

        self._build_headers(headers)

    @property
    def headers(self):
        self._read_headers()
        return self._headers

    def content(self):
        self._read_headers()
        if self._leftover:
            yield self._leftover
        for chunk in self._generator:
            yield chunk
        self._fully_read = True
