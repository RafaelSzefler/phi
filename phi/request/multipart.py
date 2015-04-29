# -*- coding: utf-8 -*-
from phi.request.base import BaseRequest


class MultipartRequest(BaseRequest):
    MAX_BATCH_SIZE = 2**13

    def content_iterator(self):
        read = 0
        max_read = self.content_length

        while read < max_read:
            read_size = min(max_read - read, self.MAX_BATCH_SIZE)
            data = self._content_stream.read(read_size)
            read += read_size
            yield data

            # TODO: headers and stuff
