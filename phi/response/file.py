# -*- coding: utf-8 -*-
from mimetypes import guess_type

from phi.response.finite import FiniteResponse


class FileResponse(FiniteResponse):

    def __init__(self, path):
        super(FileResponse, self).__init__()
        with open(path, "rb") as fo:
            self.content = fo.read()
        self.content_length = len(self.content)
        self.content_type = guess_type(path)[0]
