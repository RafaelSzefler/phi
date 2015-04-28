# -*- coding: utf-8 -*-
from phi import Application, URLRouter

url_router = URLRouter()
application = Application(
    url_router=url_router,
)
