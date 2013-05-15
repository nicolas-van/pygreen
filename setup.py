#! /usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup
import os.path

setup(name='pygreen',
      version='1.0.0',
      description='PyGreen',
      author='Nicolas Vanhoren',
      author_email='nicolas.vanhoren@unknown.com',
      url='https://github.com/nicolas-van/pygreen',
      py_modules = ['pygreen'],
      packages=[],
      scripts=["pygreen"],
      long_description="A micro web framework/static web site generator.",
      keywords="",
      license="MIT",
      classifiers=[
          ],
      install_requires=[
        "bottle >= 0.11.6",
        "mako >= 0.8.0",
        "argparse",
        ],
     )

