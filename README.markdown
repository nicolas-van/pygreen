
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

PyGreen can also exports all the files of you current folder after having the
.html files processed by Mako. To do so, type this command:

    pygreen gen <output_folder>

This can be useful to post your files on Github Pages or any other free static
files hosting services.

## FAQ

### How to avoid some mako templates files to be generated?

This is a common case if you use inheritance or macros. To avoid files to be
generated when using pygreen serve, name them with the .mako extension. They
will not be exported.

### What if I want to generate a list of html files dynamically?

As an example you want to make a blog with a list of posts. Each post is
represented by a single html file. You want to aggregate those posts to
generate multiple pages that each show a certain number of posts.

You could, like in PHP, create a single file ... (TODO)
