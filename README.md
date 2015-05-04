# phi

It's a mini web framework based on Django style. It's simple and fully
compatible with Python2.7 and Python3.x (tested with Python3.4).

The idea is based on simplicity and Single Responsibility Principle to allow
web hackers to write a code that is simple and easy to maintain/test.

## usage

You can have a look at `/examples` to see how to use it. I will list some
simple examples here:

**urls.py**

```
from phi import URLRouter, HttpResponse

url_router = URLRouter()

def home(request):
    return HttpResponse("""
      <!DOCTYPE html>
      <head></head>
      <body>
          <div><strong>Hello World!</strong></div>
      </body>
    """)

url_router.add_route("home", "/", home)
```

**main.py**

```
from phi import Application
from urls import url_router

application = Application(url_router=url_router)
```

Now you just simply bind `application` to any WSGI server.
