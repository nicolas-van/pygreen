#!/usr/bin/env python

from __future__ import division, absolute_import, print_function, unicode_literals

import unittest
import pygreen
import shutil
import os
import os.path

_folder = os.path.join(os.path.dirname(__file__), "tests")
_output = os.path.join(_folder, "output")

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        os.makedirs(_output)
        self.pygreen = pygreen.PyGreen()

    def tearDown(self):
        self.pygreen = None
        shutil.rmtree(_output)

    def test_static_get(self):
        self.pygreen.set_folder(os.path.join(_folder, "input_static_get"))
        value = self.pygreen.get("test.txt")
        self.assertEqual(value.strip(), b"test")

    def test_mako(self):
        self.pygreen.set_folder(os.path.join(_folder, "input_mako"))
        value = self.pygreen.get("test.html")
        self.assertEqual(value.strip(), b"3+2=5")

    def test_gen(self):
        self.pygreen.set_folder(os.path.join(_folder, "input_gen"))
        value = self.pygreen.gen_static(_output)
        with open(os.path.join(_output, "test.txt"), "rb") as _file:
            value = _file.read()
        self.assertEqual(value.strip(), b"test")
        with open(os.path.join(_output, "test.html"), "rb") as _file:
            value = _file.read()
        self.assertEqual(value.strip(), b"3+2=5")

    def test_markdown(self):
        self.pygreen.set_folder(os.path.join(_folder, "input_markdown"))
        value = self.pygreen.get("test.html")
        self.assertEqual(value.strip(), b"<h1>Test</h1>")

if __name__ == '__main__':
    unittest.main()
