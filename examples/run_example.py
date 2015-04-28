# -*- coding: utf-8 -*-
import sys
import importlib
from wsgiref.simple_server import make_server

if __name__ == "__main__":
    module = sys.argv[1]
    module = module.replace(".py", "").replace("/", ".")
    lib = importlib.import_module(module)
    server = make_server("", 8000, lib.application)
    server.serve_forever()
