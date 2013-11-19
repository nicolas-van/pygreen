#! /usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup
import os.path

setup(name='pygreen',
      version='2.0.0-beta.2',
      description='PyGreen',
      author='Nicolas Vanhoren',
      author_email='nicolas.vanhoren@unknown.com',
      url='http://pygreen.neoname.eu',
      py_modules = ['pygreen'],
      packages=[],
      scripts=["pygreen"],
      long_description="A micro web framework/static web site generator.",
      keywords="",
      license="MIT",
      classifiers=[
          ],
      install_requires=[
        "flask >= 0.10.1",
        "mako >= 0.8.0",
        "argparse",
        "markdown",
        ],
     )

