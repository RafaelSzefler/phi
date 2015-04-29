# -*- coding: utf-8 -*-
import re

from six import iterkeys
from six.moves.urllib.parse import parse_qs, unquote

DIVIDE_RE = re.compile(r"\w+|\W+")


class CaseInsensitiveDict(dict):
    def __init__(self):
        super(CaseInsensitiveDict, self).__init__()

    def __getitem__(self, key):
        key = key.lower()
        return super(CaseInsensitiveDict, self).__getitem__(key)

    def __setitem__(self, key, value):
        key = key.lower()
        super(CaseInsensitiveDict, self).__setitem__(key, value)

    def __delitem__(self, key):
        key = key.lower()
        super(CaseInsensitiveDict, self).__delitem__(key)

    def __contains__(self, key):
        key = key.lower()
        return super(CaseInsensitiveDict, self).__contains__(key)

    def get(self, key, *args, **kwargs):
        key = key.lower()
        return super(CaseInsensitiveDict, self).get(key, *args, **kwargs)

    def pop(self, key, *args, **kwargs):
        key = key.lower()
        return super(CaseInsensitiveDict, self).pop(key, *args, **kwargs)


def capitalize_first_letter(word):
    return word[:1].upper() + word[1:]


def capitalize_first_letters_in_sentence(sentence):
    return "".join(
        capitalize_first_letter(word) for word in DIVIDE_RE.findall(sentence)
    )


def get_status_from_exc(e):
    return e.status if hasattr(e, "status") else 500


def parse_query_string(qs):
    data = unquote(qs)
    data = parse_qs(data)
    keys = list(iterkeys(data))
    for key in keys:
        value = data[key]
        try:
            value[1]
        except IndexError:
            data[key] = value[0]
    return data
