# -*- coding: utf-8 -*-
from phi.request.multipart.joined_stream import JoinedStream

CRLF = b"\r\n"
PBOUNDARY = b"{crlf}--{}{crlf}"
FBOUNDARY = b"{crlf}--{}--{crlf}"


def dry_generator(generator):
    for _ in generator:
        pass


class BoundaryReader(object):
    MIN_BUFFER_SIZE = 128

    def __init__(self, stream, boundary, content_length):
        self._is_dry = False
        self._final_boundary_seen = False
        self._read = 0
        self._stream = JoinedStream([stream])
        self._boundary = boundary
        self._partial_boundary = CRLF + b"--" + boundary + CRLF
        self._final_boundary = CRLF + b"--" + boundary + b"--" + CRLF
        self._boundary_len = len(self._final_boundary)
        self._size = content_length

    def is_dry(self):
        return self._is_dry

    def initialize(self, buffer_size=None):
        if buffer_size is None:
            buffer_size = self.MIN_BUFFER_SIZE

        self._leftover = self._read_chunk(buffer_size)

    def fully_read(self):
        return self._read == self._size

    def _read_chunk(self, buffer_size):
        left = self._size - self._read
        if left <= 0:
            return b""
        to_read = min(left, buffer_size)
        data = self._stream.read(to_read)
        self._read += to_read
        return data

    def read_until_next_boundary(self, buffer_size):
        if buffer_size < self.MIN_BUFFER_SIZE:
            raise ValueError("Buffer size too small!")

        if self.is_dry():
            yield b""
            return

        current_chunk = self._leftover
        while True:
            next_chunk = self._read_chunk(buffer_size)
            extended_chunk = current_chunk + next_chunk

            if not self._final_boundary_seen:
                before, separator, after = extended_chunk.partition(
                    self._final_boundary
                )
                if separator:
                    self._final_boundary_seen = True
                    self._read = self._size
                    self._leftover = before
                    current_chunk = before
                    continue

            before, separator, after = extended_chunk.partition(
                self._partial_boundary
            )

            if separator:
                self._leftover = after
                yield before
                return

            self._leftover = next_chunk
            yield current_chunk
            current_chunk = next_chunk

            if self._read == self._size:
                self._is_dry = True
                return
