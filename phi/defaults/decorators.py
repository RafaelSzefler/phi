# -*- coding: utf-8 -*-
from decorator import decorator
from phi.exceptions import HttpMethodNotAllowed
from phi.request.base import BaseRequest


def dummy_decorator(fn):
    return fn


def get_request_object(args):
    # This is so that we can use decorators with both functions and methods.
    for arg in args:
        if isinstance(arg, BaseRequest):
            return arg
    raise AttributeError("No request object passed to controller!")


def requires_methods(methods):
    if not methods:
        return dummy_decorator

    @decorator
    def wrapper(fn, *args, **kwargs):
        request = get_request_object(args)
        if request.method not in methods:
            msg = "Handler [{fn}] does not allow {method} method."
            msg = msg.format(fn=fn.__name__, method=request.method)
            raise HttpMethodNotAllowed(msg)
        return fn(*args, **kwargs)

    return wrapper
