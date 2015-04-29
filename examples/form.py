# -*- coding: utf-8 -*-
from phi import Application, URLRouter, HttpResponse

from common import FORM_HTML

url_router = URLRouter()


def home(request):
    return HttpResponse(FORM_HTML)

url_router.add_route("home", "/", home)


def submit(request):
    return HttpResponse(FORM_HTML)

url_router.add_route("submit", "/form", submit)


application = Application(
    url_router=url_router,
)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("", 8000, application)
    server.serve_forever()
