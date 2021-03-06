# -*- coding: utf-8 -*-
from phi import Application, URLRouter, HttpResponse

from common import UPLOAD_HTML

url_router = URLRouter()


def home(request):
    return HttpResponse(UPLOAD_HTML)

url_router.add_route("home", "/", home)


def form(request):
    attachments = request.attachments()
    for attachment in attachments:
        print
        print attachment.headers
        print "*"*30
        for chunk in attachment.content():
            print chunk
        print
        print "="*35
        print

    return HttpResponse(UPLOAD_HTML)

url_router.add_route("form", "/form", form)


application = Application(
    url_router=url_router,
)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("", 8000, application)
    server.serve_forever()
