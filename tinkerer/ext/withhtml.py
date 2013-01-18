"""An extension which provides support for attaching static html
pages in your docs dir
To use this just add this module to your extensions list in conf.py file, like:

    extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus', 'tinkerer.ext.withhtml']

and add your html files to *docs* directory.
Then when tinkerer will build your portal, it will copy all html files
(and render .rst files) from *docs* to *blog/html/docs*.
"""

import os
import shutil


def sphinx_extension(app, exception):
    "Wrapped up as a Sphinx Extension"

    if not app.builder.name in ("html", "dirhtml"):
        return

    docs = os.path.join(app.srcdir, 'docs')
    if not os.path.isdir(docs):
        return
    docs_out = os.path.join(app.outdir, 'docs')
    if not os.path.isdir(docs_out):
        os.mkdir(docs_out)

    print("Searching for *.html documents in %s" % docs)
    copied = []
    for fname in os.listdir(docs):
        fname = os.path.join(docs, fname)
        if os.path.isfile(fname) and fname.endswith('.html'):
            shutil.copy(fname, docs_out)
            copied.append(fname)
    print("copied %s files" % copied)



def setup(app):
    "Setup function for Sphinx Extension"

    app.add_config_value("copy_html_files", True, '')
    app.connect("build-finished", sphinx_extension)
