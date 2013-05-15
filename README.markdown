
# PyGreen

A micro web framework/static web site generator.

PyGreen is a simple tool to generate small web sites. The concept is to put
all files to serve in a folder and invoke the
[Mako](http://www.makotemplates.org/) template engine on all .html files. The
result is quite similar to a classic PHP application, but with the good
features of the Mako templates (like inheritance) and the cool syntax of
Python.

## Quick Start

To install:

    sudo easy_install pygreen

To launch and serve files:

    pygreen serve

The above command will serve the files located in the current folder. All
files with the .html extension will also be processed by Mako. So if the
current folder contains a file index.html with the following code:

    <p>Hello, my age is ${30 - 2}.</p>

When going to http://localhost:8080, you will see:

    <p>Hello, my age is 28.</p>

PyGreen can also export all the files of you current folder after having the
.html files processed by Mako. To do so, type this command:

    pygreen gen <output_folder>

This can be useful to post your files on Github Pages or any other free static
files hosting services.

## FAQ

### How to avoid some mako templates files to be generated?

This is a common case if you use inheritance or macros. To avoid files to be
generated when using pygreen serve, name them with the .mako extension. They
will not be exported.

### What else?

There is nothing else. PyGreen was created to be a static web site generator
more effective than existing ones. The problem of existing site generators
like Jekyll or Hyde is that they have a fixed number of features. Even if
their creators try to add new features those will not be correctly documented,
so the users do not know how to use them.

The fact that PyGreen has a small set of features **is a feature**. PyGreem is
just Mako templates served using the [Bottle](http://bottlepy.org/) 
micro-framework. Mako templates can contain Python so if you need to do complex
stuff just import whatever you need, type the code and get the job done. You
need to generate new files dynamically or do anything that is not supported?
Import the pygreen module, extend the Bottle object with new routes and you
can do anything you want. You don't need documentation for that, PyGreen
is 100 lines long, anyone can read it and understand it.

If you know how to program, just typing the code to generate the html you want
is easier than trying to understand a tool dedicated to the task. PyGreen just
makes it easier to start even faster.
