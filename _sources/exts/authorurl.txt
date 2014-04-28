Author URL
==========
.. highlight:: python

This adds a link to every author name in postmeta.

Simply add it to your extensions in ``conf.py``: ::

  # Add other Sphinx extensions here
  extensions = [..., 'authorurl']

and specify a URL: ::

  author_url = 'http://www.yoursite.com/pages/about.html#about-me'
