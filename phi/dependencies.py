# -*- coding: utf-8 -*-
try:
    import simplejson as json
except ImportError:
    import json

try:
    import msgpack
except ImportError:
    msgpack = None
