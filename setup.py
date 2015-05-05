# -*- coding: utf-8 -*-
import re
from os import path

from setuptools import setup, find_packages

ROOT = path.dirname(__file__)
name = "phi"
author = "Rafael Szefler"
author_email = "rafael.szefler@gmail.com"
description = "Mini WebFramework"


def read_requirements(filename):
    full_path = path.join(ROOT, filename)
    requirements = []
    with open(full_path, "rb") as fo:
        for line in fo:
            line = line.decode("utf-8").strip()
            if line:
                requirements.append(line)
    return requirements


def get_version():
    init_file = path.join(ROOT, name, "__init__.py")
    pattern = re.compile('version = "(?P<ver>.*?)"')
    with open(init_file, "rb") as fo:
        for line in fo:
            line = line.decode("utf-8")
            match = pattern.match(line)
            if match:
                return match.group("ver")
    return None


def get_packages():
    pkgs = [name + "." + pkg for pkg in find_packages(name)]
    return [name] + pkgs


setup(
    name=name,
    version=get_version(),
    description=description,
    author=author,
    author_email=author_email,
    install_requires=read_requirements("requirements.txt"),
    packages=get_packages()
)
