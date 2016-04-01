# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import tempfile
import io


class TextTempFile(object):
    """
    A wrapper around a named temporary file with encoded text interface and
    initial content.

    See ```tempfile.NamedTemporaryFile``` and ```io.open```.

    Examples:
        >>> with TextTempFile("Hello \u2603", encoding="utf-8") as f:
        ...     with io.open(f.name, "rt") as f2:
        ...         init_text = f2.read()
        ...     f.write("\nMore text")
        ...     f.flush()
        ...     with io.open(f.name, "rt") as f2:
        ...         more_text = f2.read()
        ...     with io.open(f.name, "rb") as f2:
        ...         raw_bytes = f2.read()
        ...
        >>> print(init_text)
        u'Hello \u2603'
        >>> print(more_text)
        u'Hello \u2603\nMore text'
        >>> print(raw_bytes)
        'Hello \xe2\x98\x83\nMore text'
    """
    def __init__(self, init_text=None,
                 buffering=-1, encoding=None, errors=None, newline=None,
                 suffix="", prefix="tmp", dir=None,
                 delete=True):
        """
        Args:
            init_content (Optional[unicode]): Initial content to write to the
                temporary file.
                Defaults to ```None``` (empty file).
            buffering, encoding, errors, newline: See ```io.open```.
            suffix, prefix, dir: See ```tempfile.NamedTemporaryFile```.
            delete (Optional[bool]): Delete underlying file on close.
                Defaults to ```True```.
        """
        (self._file_fd, self._file_name) = tempfile.mkstemp(
                suffix=suffix,
                prefix=prefix,
                dir=dir,
                text=False)
        self._file = io.open(self._file_name, mode="w+t", buffering=buffering,
                             encoding=encoding, errors=errors, newline=newline)
        self._delete = delete
        if init_text is not None:
            self._file.write(init_text)
            self._file.flush()

    def __getattr__(self, name):
        return getattr(self._file, name)

    def __setattr__(self, name, value):
        if name in ["_file", "_file_fd", "_file_name", "_delete"]:
            super(TextTempFile, self).__setattr__(name, value)
        else:
            self._file.__setattr__(name, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def name(self):
        return self._file_name

    def close(self):
        self._file.close()
        if self._delete:
            os.remove(self._file_name)
