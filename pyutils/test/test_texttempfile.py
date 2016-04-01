#! /bin/python
# -*- coding: utf-8 -*-
"""
Module docstring
"""

from __future__ import unicode_literals, print_function

import unittest
import io
import os.path
import tempfile

from pyutils.texttempfile import TextTempFile


UNICODE_SNOWMAN = "\u2603"
UNICODE_PILE_OF_POO = "\u1F4A9"


class TestTextTempFile(unittest.TestCase):
    init_text = "Hello " + UNICODE_SNOWMAN
    more_text = "\nSome more text " + UNICODE_PILE_OF_POO

    def test_name(self):
        f = TextTempFile()
        self.assertIsInstance(f.name, unicode, "file name not unicode string")
        name_prefix = os.path.join(tempfile.gettempdir(),
                tempfile.gettempprefix())
        self.assertTrue(f.name.startswith(name_prefix),
                "file name does not start with '{}'".format(name_prefix))
        with self.assertRaises(AttributeError):
            f.name = "new_name"

    def test_file_creation(self):
        f = TextTempFile()
        self.assertTrue(os.path.isfile(f.name),
                "underlying file does not exist")
        f.close()

    def test_file_delete_on_close(self):
        f = TextTempFile()
        self.assertFalse(f.closed, "file marked as closed")
        f.close()
        self.assertTrue(f.closed, "file marked as open")
        self.assertFalse(os.path.isfile(f.name), "underlying file not deleted")

    def test_file_no_delete_on_close(self):
        f = TextTempFile(delete=False)
        self.assertFalse(f.closed, "file marked as closed")
        f.close()
        self.assertTrue(f.closed, "file marked as open")
        self.assertTrue(os.path.isfile(f.name), "underlying file deleted")

    def test_with_statement(self):
        with TextTempFile() as f:
            self.assertFalse(f.closed, "file marked as closed")
            self.assertTrue(os.path.isfile(f.name),
                "underlying file does not exist")
        self.assertTrue(f.closed, "file marked as open")
        self.assertFalse(os.path.isfile(f.name), "underlying file not deleted")

    def test_empty_init(self):
        with TextTempFile(encoding="utf-8") as f:
            with io.open(f.name, "rb") as f2b:
                self.assertEqual(f2b.read(), b"", "file not empty")

    def test_non_empty_init(self):
        with TextTempFile(self.init_text, encoding="utf-8") as f:
            with io.open(f.name, "rt", encoding="utf-8") as f2t:
                text_content = f2t.read()
                self.assertEqual(text_content, self.init_text,
                        "bad init text: '{}'' != '{}'"
                        .format(text_content, self.init_text))
            with io.open(f.name, "rb") as f2b:
                byte_content = f2b.read()
                self.assertEqual(byte_content, self.init_text.encode("utf-8"),
                        "bad init bytes: b'{}' != b'{}'"
                        .format(byte_content.decode("utf-8"), self.init_text))

    def test_write(self):
        with TextTempFile(self.init_text, encoding="utf-8") as f:
            f.write(self.more_text)
            f.flush()
            with io.open(f.name, "rt", encoding="utf-8") as f2t:
                text_content = f2t.read()
                self.assertEqual(text_content, self.init_text + self.more_text,
                        "bad init text: '{}'' != '{}'"
                        .format(text_content, self.init_text))
            with io.open(f.name, "rb") as f2b:
                byte_content = f2b.read()
                self.assertEqual(byte_content,
                        (self.init_text + self.more_text).encode("utf-8"),
                        "bad init bytes: b'{}' != b'{}'"
                        .format(byte_content.decode("utf-8"), self.init_text))
