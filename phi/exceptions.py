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


class HttpForbidden(HttpException):
    status = 403


class HttpNotFound(HttpException):
    status = 404
