"""An extension which provides support for github pages.
By default Github pages prohibits names starting with '_'.
But sphinx requires them. It is internal strategy to use '_'
for directory with static content.
To change this behaviour you need to add '.nojekyll' file in a base
direcotry. This extension automates the process.

To use this just add this module to your extensions list in conf.py file, like:

    extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus', 'tinkerer.ext.withhtml']
"""

import os


def sphinx_extension(app, exception):
    "Wrapped up as a Sphinx Extension"
    jekyll_file = os.path.join(app.outdir, '.nojekyll')
    open(jekyll_file, 'w').close()
    print("writed %s file to prevent github blocking _* directories" % jekyll_file)


def setup(app):
    "Setup function for Sphinx Extension"

    app.add_config_value("github.nojekyll", True, '')
    app.connect("build-finished", sphinx_extension)
