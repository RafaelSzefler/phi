# -*- coding: utf-8 -*-
from os import path

from phi import Application, URLRouter, FileResponse

url_router = URLRouter()

FILE_PATH = path.realpath(path.dirname(__file__))
FILE_PATH = path.join(FILE_PATH, "test.js")


def home(request):
    return FileResponse(FILE_PATH)

url_router.add_route("home", "/", home)


application = Application(
    url_router=url_router,
)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("", 8000, application)
    server.serve_forever()
