# -*- coding: utf-8 -*-
from phi.exceptions import HttpNotFound


class ActionController(object):
    def __init__(self, action_name="action"):
        self._action_name = action_name

    def __call__(self, request, **kwargs):
        action = kwargs.pop(self._action_name, None)

        if not action or action.startswith("_") or not hasattr(self, action):
            raise HttpNotFound

        handler = getattr(self, action)
        if not callable(handler):
            raise HttpNotFound

        return handler(request, **kwargs)
