
from __future__ import unicode_literals

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
        self.assertEqual(value.strip(), "test")

    def test_mako(self):
        self.pygreen.set_folder(os.path.join(_folder, "input_mako"))
        value = self.pygreen.get("test.html")
        self.assertEqual(value.strip(), "3+2=5")

if __name__ == '__main__':
    unittest.main()
