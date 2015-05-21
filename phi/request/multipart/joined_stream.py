# -*- coding: utf-8 -*-


class JoinedStream(object):
    def __init__(self, streams):
        self.streams = streams

    def read(self, amount_to_read):
        read = 0
        chunk = b""
        while True:
            if not self.streams:
                break

            stream = self.streams[0]
            left_to_read = amount_to_read - read
            data = stream.read(left_to_read)
            chunk += data
            read += len(data)
            if read == amount_to_read:
                break

            self.streams.pop(0)

        return chunk
