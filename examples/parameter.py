# -*- coding: utf-8 -*-
from phi import Application, URLRouter, HttpResponse, JsonResponse

from common import HELLO_WORLD_HTML

url_router = URLRouter()


def home(request):
    return HttpResponse(HELLO_WORLD_HTML)

url_router.add_route("home", "/", home)


def test(request, param):
    return JsonResponse({"param": param})

url_router.add_route("test", "/word/{param}/", test)


def numeric(request, param):
    return JsonResponse({"param": param})

url_router.add_route("numeric", "/numeric/{param:\d+}/", numeric)


application = Application(
    url_router=url_router,
)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("", 8000, application)
    server.serve_forever()
