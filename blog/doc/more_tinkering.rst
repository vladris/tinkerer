More Tinkering
==============

Enabling Disqus Comments
------------------------

To enable comments powered by `Disqus <http://disqus.com>`_, create a Disqus
account for your website and update ``disqus_shortname`` in ``conf.py`` with 
your Disqus shortname.

.. note::

    You will not be able to preview comments offline since comment box is 
    retrieved via JS from Disqus and the page must match your account's URL.

Enabling Google Analytics
-------------------------

.. highlight:: html

To enable `Google Analytics <http://google.com/analytics>`_ for your blog, 
setup your Google Analytics account. You will be provided some JS  code.
Add the JS code to a file in your blog's ``_static`` directory as 
``googl_analytics.js`` and create a new ``page.html`` file under your blog's 
``_templates`` directory with the following content::

   {% extends "!page.html" %}

   {% set script_files = script_files + ["_static/google_analytics.js"] %}

This will load the Google Analytics script on each page of your blog.

More information on extending templates can be found in the
`Sphinx documentation <http://sphinx.pocoo.org/templating.html#script_files>`_.

RSS
---

Tinkerer generates an RSS feed as ``blog/html/rss.html``. A link to the feed is 
automatically added to the navigation bar. In case you use a service like
`FeedBurner <http://www.feedburner.com>`_, you can change the ``rss_service``
value in ``conf.py`` to the address of your feed and Tinkerer will change the
link to point to the provided address.

Favicon
-------

Tinkerer uses a default ``tinkerer.ico`` as your blog's favicon. You can 
replace this with your own icon by placing your icon under the blog's 
``_static`` directory and changing the ``html_favicon`` value to the name
of your icon file (path is not required, only filename).

Theming
-------

Tinkerer comes with three themes: *modern* - the default theme, *minimal* - a
minimalist black and white theme and a base *tinkerbase* theme from which the
others inherit. *Tinkerbase* is not styled, rather it implements the basic
layout. Due to the inherent differences between documentation and blogs, 
Sphinx themes are not fully compatible with Tinkerer.

To tinker with the look of your blog, you have two options:

Add a custom stylesheet
~~~~~~~~~~~~~~~~~~~~~~~

Create your own ``style.css`` (filename is not important) and place it under 
the blog's ``_static`` directory and create a new ``page.html`` file under 
your blog's ``_templates`` directory with the following content::

    {% extends "!page.html" %}

    {% set css_files = css_files + ["_static/style.css"] %}

More information on extending templates can be found 
`here <http://sphinx.pocoo.org/templating.html#css_files>`_.

Create your own theme
~~~~~~~~~~~~~~~~~~~~~

Tinkerer themes should inherit from the *tinkerbase* theme. For more information 
on creating themes see 
`Creating themes <http://sphinx.pocoo.org/theming.html#creating-themes>`_.

Extensions
----------

To add a Sphinx extension to your blog, update the ``extensions`` list in
``conf.py``. The ``tinkerer.ext.blog`` extension contains the Tinkerer logic to
enable blogging with Sphinx and the ``tinkerer.ext.disqus`` extension is the 
Disqus comment handler.

Sidebar
-------

The ``html_sidebars`` list contains the list of templates to be rendered on the 
sidebar. Tinkerer includes ``recent.html`` and ``searchbox.html`` by default.

**recent.html** 

    Displays a list of the most recent posts.

**searchbox.html**

    This is the Sphinx quicksearch box.    

`More information on sidebars <http://sphinx.pocoo.org/config.html#confval-html_sidebars>`_.

Back to :ref:`tinkerer_reference`.

