# -*- coding: utf-8 -*-

"""
Note on json encoding:

In a json string sequences like "\\u2603" (written in
plain ASCII characters) are valid and decoded into unicode characters. This is
part of the json spec (not only the Python module).

Otherwise unicode characters can be encoded using non-ascii encodings like
utf-8, giving for example "\\xe2\\x98\\x83".

With the Python json implementation:
- When loading, both types of byte streams will be correctly decoded.
- When dumping, the output style is controlled by the ensure_ascii argument. The
  default is ensure_ascii=True and will yield the "\\u"-style, ascii encoding. If
  ensure_ascii is False, dumping will yield the "\\x"-style, non-ascii encoding.

See: http://stackoverflow.com/questions/4184108/python-json-dumps-cant-handle-utf-8
"""

from __future__ import unicode_literals, print_function

import json
import io


def load_file(filename, encoding="utf-8"):
    with io.open(filename, "rb") as json_file:
        return json.load(json_file, encoding=encoding)


def dump_file(obj, filename, encoding="utf-8"):
    with io.open(filename, "wb") as json_file:
        return json.dump(obj, json_file, encoding=encoding)
