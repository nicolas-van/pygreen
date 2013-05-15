
from __future__ import unicode_literals

import bottle
import os.path
import webtest
from mako.template import Template
from mako.lookup import TemplateLookup
import os
import os.path
import cStringIO

class PyHP:

    def __init__(self):
        self.app = bottle.Bottle()
        self.folder = "."
        self.template_exts = set(["html"])

        self.templates = TemplateLookup()
        self._template_inited = False

        def base_lister():
            files = []
            for dirpath, dirnames, filenames in os.walk(self.folder):
                for f in filenames:
                    absp = os.path.join(dirpath, f)
                    path = os.path.relpath(absp, self.folder)
                    print path
                    files.append(path)
            return files
        self.file_listers = [base_lister]

        @self.app.route('/', method=['GET', 'POST', 'PUT', 'DELETE'])
        @self.app.route('/<path:path>', method=['GET', 'POST', 'PUT', 'DELETE'])
        def hello(path="index.html"):
            if path.split(".")[-1] in self.template_exts:
                return self.templates.get_template(path).render(pyhp=pyhp, path=path)
            return bottle.static_file(path, root=self.folder)

    def _check_template_path(self):
        if not self._template_inited:
            self.templates.directories.append(self.folder)
            self._template_inited = True

    def run(self, **kwargs):
        self._check_template_path()
        bottle.run(self.app, **kwargs)

    def get(self, path):
        out = b"".join(pyhp.app({
            'PATH_INFO': "/%s" % path,
            'REQUEST_METHOD': "GET",
            'wsgi.errors':cStringIO.StringIO()
            }, lambda *args: None))
        return out

    def gen_static(self, output_folder):
        self._check_template_path()
        files = []
        for l in self.file_listers:
            files += l()
        for f in files:
            print "get", f
            content = self.get(f)
            with open(os.path.join(output_folder, f), "w") as file_:
                file_.write(content)

pyhp = PyHP()

def main():
    pyhp.folder = "site"
    #pyhp.run()
    pyhp.gen_static("output")

if __name__ == "__main__":
    main()
