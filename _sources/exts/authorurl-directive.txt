Author URL Directive
====================
.. highlight:: python

This adds a link to the author name in postmeta.

Simply add it to your extensions in ``conf.py``: ::

  # Add other Sphinx extensions here
  extensions = [..., 'authorurl-directive']

and specify a default URL: ::

  author_url = 'http://www.yoursite.com/pages/about.html#about-me'

Usage:

  Add ``.. author_url:: default`` or ``.. author_url:: http://site.com/``
  to posts where you want to add a website link to an author.
