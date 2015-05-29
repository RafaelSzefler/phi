# -*- coding: utf-8 -*-


class PhiException(Exception):
    pass


class RoutingException(PhiException):
    pass


class ValidationError(PhiException):
    pass


class HttpException(PhiException):
    status = 500


class HttpBadRequest(HttpException):
    status = 400


class HttpUnauthorized(HttpException):
    status = 401


class HttpForbidden(HttpException):
    status = 403


class HttpNotFound(HttpException):
    status = 404


class HttpMethodNotAllowed(HttpException):
    status = 405
