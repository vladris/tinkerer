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
Add the JS code (excluding any ``<script>`` tags) to a file in your blog's
``_static`` directory as ``google_analytics.js`` and create a new
``page.html`` file under your blog's ``_templates`` directory with the
following content::

   {% extends "!page.html" %}

   {% set script_files = script_files + ["_static/google_analytics.js"] %}

This will load the Google Analytics script on each page of your blog.

More information on extending templates can be found in the
`Sphinx documentation <http://sphinx.pocoo.org/templating.html#script_files>`_.

Localization
------------

.. highlight:: python

By default, Tinkerer is built using English language. Tinkerer is currently
localized in Spanish and Catalan. To change localization, add the following
line to your ``conf.py`` for Spanish::

   language = "es"

or for Catalan::

   language = "ca"

.. highlight:: html

RSS
---

Tinkerer generates an RSS feed as ``blog/html/rss.html``. A link to the feed is
automatically added to the navigation bar. In case you use a service like
`FeedBurner <http://www.feedburner.com>`_, you can change the ``rss_service``
value in ``conf.py`` to the address of your feed and Tinkerer will change the
link to point to the provided address. Set ``rss_max_items`` to the number of
items to include in the feed, or ``0`` to include everything.

Favicon
-------

Tinkerer uses a default ``tinkerer.ico`` as your blog's favicon. You can
replace this with your own icon by placing your icon under the blog's
``_static`` directory and changing the ``html_favicon`` value to the name
of your icon file (path is not required, only filename).

.. _landingpage:

Landing Page
------------

By default, the landing page for a blog is the first aggregated page,
containing the latest 10 posts. This can be changed by setting ``landing_page``
in ``conf.py`` to a different page under the blog's ``/pages`` directory. For
example, to land users on ``/pages/about.html``, update ``landing_page = None``
to ``landing_page = "about"``.

The title of the first aggregated page is "Home". To change the title from
"Home" to something else, change the ``first_page_title`` setting in
``conf.py``.

.. _sidebar:

Sidebar
-------

The ``html_sidebars`` list contains the list of templates to be rendered on the
sidebar. Tinkerer includes ``recent.html`` and ``searchbox.html`` by default. A
list of categories, a list of tags and a tag cloud are also part of the Tinkerer
distribution and can be easily added by updating the ``html_sidebars`` setting in
``conf.py`` to include the corresponding files.

**recent.html**

    Displays a list of the most recent posts.

**searchbox.html**

    This is the equivalent of the Sphinx quicksearch box.

**categories.html**

    Displays a list of categories under which posts were filed.

**tags.html**

    Displays a list of tags under which posts were filed.

**tags_cloud.html**

    Tag cloud.

`More information on sidebars <http://sphinx.pocoo.org/config.html#confval-html_sidebars>`_.


Back to :ref:`tinkerer_reference`.

