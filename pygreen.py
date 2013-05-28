#! /usr/bin/python

# PyGreen
# Copyright (c) 2013, Nicolas Vanhoren
# 
# Released under the MIT license
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals

import bottle
import os.path
from mako.lookup import TemplateLookup
import os
import os.path
import wsgiref.handlers
import sys
import logging
import re
import argparse
import sys
import markdown

_logger = logging.getLogger(__name__)

class PyGreen:

    def __init__(self):
        # the Bottle application
        self.app = bottle.Bottle()
        # a set of strings that identifies the extension of the files
        # that should be processed using Mako
        self.template_exts = set(["html"])
        # the folder where the files to serve are located. Do not set
        # directly, use set_folder instead
        self.folder = "."
        # the TemplateLookup of Mako
        self.templates = TemplateLookup(directories=[self.folder], \
            imports=["from markdown import markdown"])
        # A list of regular expression. Files whose the name match
        # one of those regular expressions will not be outputed when generating
        # a static version of the web site
        self.file_exclusion = [r".*\.mako", r"(^|.*\/)\..*"]
        def base_lister():
            files = []
            for dirpath, dirnames, filenames in os.walk(self.folder):
                for f in filenames:
                    absp = os.path.join(dirpath, f)
                    path = os.path.relpath(absp, self.folder)
                    good = True
                    for ex in self.file_exclusion:
                        if re.match(ex, path):
                            good = False
                            continue
                    if good:
                        files.append(path)
            return files
        # A list of function. Each function must return a list of paths
        # of files to export during the generation of the static web site.
        # The default one simply returns all the files contained in the folder.
        # It is necessary to define new listers when new routes are defined
        # in the Bottle application, or the static site generation routine
        # will not be able to detect the files to export.
        self.file_listers = [base_lister]

        @self.app.route('/', method=['GET', 'POST', 'PUT', 'DELETE'])
        @self.app.route('/<path:path>', method=['GET', 'POST', 'PUT', 'DELETE'])
        def hello(path="index.html"):
            if path.split(".")[-1] in self.template_exts:
                return self.templates.get_template(path).render(pygreen=pygreen)
            return bottle.static_file(path, root=self.folder)

    def set_folder(self, folder):
        """
        Sets the folder where the files to serve are located.
        """
        self.folder = folder
        self.templates.directories[0] = folder

    def run(self, **kwargs):
        """
        Launch a development web server.
        """
        kwargs.setdefault("host", "0.0.0.0")
        bottle.run(self.app, **kwargs)

    def get(self, path):
        """
        Get the content of a file, indentified by its path relative to the folder configured
        in PyGreen. If the file extension is one of the extensions that should be processed
        through Mako, it will be processed.
        """
        handler = wsgiref.handlers.SimpleHandler(sys.stdin, sys.stdout, sys.stderr, {})
        handler.setup_environ()
        env = handler.environ
        env.update({'PATH_INFO': "/%s" % path, 'REQUEST_METHOD': "GET"})
        out = b"".join(pygreen.app(env, lambda *args: None))
        return out

    def gen_static(self, output_folder):
        """
        Generates a complete static version of the web site. It will stored in 
        output_folder.
        """
        files = []
        for l in self.file_listers:
            files += l()
        for f in files:
            _logger.info("generating %s" % f)
            content = self.get(f)
            loc = os.path.join(output_folder, f)
            d = os.path.dirname(loc)
            if not os.path.exists(d):
                os.makedirs(d)
            with open(loc, "wb") as file_:
                file_.write(content)

    def cli(self, cmd_args=None):
        """
        The command line interface of PyGreen.
        """
        logging.basicConfig(level=logging.INFO, format='%(message)s')

        parser = argparse.ArgumentParser(description='PyGreen, micro web framework/static web site generator')
        subparsers = parser.add_subparsers(dest='action')

        parser_serve = subparsers.add_parser('serve', help='serve the web site')
        parser_serve.add_argument('-p', '--port', type=int, default=8080, help='folder containg files to serve')
        parser_serve.add_argument('-f', '--folder', default=".", help='folder containg files to serve')
        def serve():
            pygreen.run(port=args.port)
        parser_serve.set_defaults(func=serve)

        parser_gen = subparsers.add_parser('gen', help='generate a static version of the site')
        parser_gen.add_argument('output', help='folder to store the files')
        parser_gen.add_argument('-f', '--folder', default=".", help='folder containg files to serve')
        def gen():
            pygreen.gen_static(args.output)
        parser_gen.set_defaults(func=gen)

        args = parser.parse_args(cmd_args)
        pygreen.set_folder(args.folder)
        args.func()

pygreen = PyGreen()

if __name__ == "__main__":
    pygreen.cli()
