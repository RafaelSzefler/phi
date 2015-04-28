# -*- coding: utf-8 -*-
from phi import Application, URLRouter, HttpResponse

from common import HELLO_WORLD_HTML

url_router = URLRouter()


def home(request):
    return HttpResponse(HELLO_WORLD_HTML)

url_router.add_route("home", "/", home)


application = Application(
    url_router=url_router,
)
