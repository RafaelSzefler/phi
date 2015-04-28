from phi.response.base import BaseResponse


class FiniteResponse(BaseResponse):
    def _update_header_list_with_content_length(self, header_list):
        header_list.append(("Content-Length", str(self.content_length)))

    def _get_wsgi_content_iterator(self):
        yield self.content
