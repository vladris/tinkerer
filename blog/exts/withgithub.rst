Github Pages
------------

This extension provides support for github pages. 

By default Github Pages prohibit names starting with '_', but Sphinx requires
them. To change this behavior, a '.nojekyll' file is needed in a base 
directory. This extension handles that automatically.

To use it, download ``withgithub.py`` in your blog's ``_exts`` directory and
add ``withgithub`` module to your extensions list in `conf.py` file::

    extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus', 'withgithub']

