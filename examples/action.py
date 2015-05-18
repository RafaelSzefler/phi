# -*- coding: utf-8 -*-
from phi import Application, URLRouter, HttpResponse, ActionController

url_router = URLRouter()


class Home(ActionController):
    test = 1

    def _foo(self, request):
        return HttpResponse("_foo")

    def home(self, request):
        return HttpResponse("home")

    def blah(self, request):
        return HttpResponse("blah")

url_router.add_route("home", "/{action}/", Home())

application = Application(
    url_router=url_router,
)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("", 8000, application)
    server.serve_forever()
