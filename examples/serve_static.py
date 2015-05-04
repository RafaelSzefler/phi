# -*- coding: utf-8 -*-
from os import path

from phi import Application, URLRouter, HttpResponse, MiddlewareHandler
from phi.defaults.statics import StaticsHandler

url_router = URLRouter()
middleware_handler = MiddlewareHandler()

ROOT = path.realpath(path.dirname(__file__))


def home(request):
    return HttpResponse("OK")

url_router.add_route("home", "/", home)

middleware_handler.add_pre_handler(StaticsHandler("/statics/", ROOT))

application = Application(
    url_router=url_router,
    middleware_handler=middleware_handler
)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("", 8000, application)
    server.serve_forever()
