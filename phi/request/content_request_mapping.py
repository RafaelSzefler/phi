# -*- coding: utf-8 -*-
from phi.request.jsonr import JsonRequest
from phi.request.form import FormRequest


CONTENT_TYPE_TO_REQUEST_CLASS_MAP = {
    "application/json": JsonRequest,
    "application/x-www-form-urlencoded": FormRequest
}