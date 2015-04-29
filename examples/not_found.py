# -*- coding: utf-8 -*-
from phi import Application, URLRouter

url_router = URLRouter()
application = Application(
    url_router=url_router,
)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("", 8000, application)
