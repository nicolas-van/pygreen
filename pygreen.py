#! /usr/bin/python

#    PyGreen
#    Copyright (C) 2012 Nicolas Vanhoren
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import bottle
import os.path
import webtest
from mako.lookup import TemplateLookup
import os
import os.path
import wsgiref.handlers
import sys
import logging
import re
import argparse

_logger = logging.getLogger(__name__)

class PyGreen:

    def __init__(self):
        self.app = bottle.Bottle()
        self.folder = "."
        self.template_exts = set(["html"])

        self.templates = TemplateLookup()
        self._template_inited = False

        self.file_exclusion = [r"^.*\.mako$"]
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
        self.file_listers = [base_lister]

        @self.app.route('/', method=['GET', 'POST', 'PUT', 'DELETE'])
        @self.app.route('/<path:path>', method=['GET', 'POST', 'PUT', 'DELETE'])
        def hello(path="index.html"):
            if path.split(".")[-1] in self.template_exts:
                return self.templates.get_template(path).render(pygreen=pygreen, path=path)
            return bottle.static_file(path, root=self.folder)

    def _check_template_path(self):
        if not self._template_inited:
            self.templates.directories.append(self.folder)
            self._template_inited = True

    def run(self, **kwargs):
        self._check_template_path()
        bottle.run(self.app, **kwargs)

    def get(self, path):
        handler = wsgiref.handlers.SimpleHandler(sys.stdin, sys.stdout, sys.stderr, {})
        handler.setup_environ()
        env = handler.environ
        env.update({'PATH_INFO': "/%s" % path, 'REQUEST_METHOD': "GET"})
        out = b"".join(pygreen.app(env, lambda *args: None))
        return out

    def gen_static(self, output_folder):
        self._check_template_path()
        files = []
        for l in self.file_listers:
            files += l()
        for f in files:
            _logger.info("generating %s" % f)
            content = self.get(f)
            with open(os.path.join(output_folder, f), "w") as file_:
                file_.write(content)

pygreen = PyGreen()

def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description='PyGreen, micro web framework/static web site generator')
    subparsers = parser.add_subparsers(dest='action')

    parser_serve = subparsers.add_parser('serve', help='serve the web site')
    parser_serve.add_argument('-f', '--folder', default=".", help='folder containg files to serve')
    parser_serve.add_argument('-p', '--port', type=int, default=8080, help='folder containg files to serve')
    def serve():
        pygreen.folder = args.folder
        pygreen.run(port=args.port)
    parser_serve.set_defaults(func=serve)

    parser_gen = subparsers.add_parser('gen', help='generate a static version of the site')
    parser_gen.add_argument('output', help='folder to store the files')
    parser_gen.add_argument('-f', '--folder', default=".", help='folder containg files to serve')
    def gen():
        pygreen.folder = args.folder
        pygreen.gen_static(args.output)
    parser_gen.set_defaults(func=gen)

    args = parser.parse_args()
    args.func()

    pygreen.folder = "site"
    #pygreen.run()
    #pygreen.gen_static("output")

if __name__ == "__main__":
    main()
