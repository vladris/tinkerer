Theming
=======

Tinkerer comes with a base *boilerplate* theme. This is an unstyled theme based
on HTML5 Boilerplate. Custom themes should inherit from it.

The default Tinkerer theme is *flat*, which is based on the *boilerplate*.

Tinkerer also ships with *modern5*, *minimal5*, *responsive* and *dark* themes
(preview on the sidebar).

Tweaking the flat theme
-----------------------

.. highlight:: python

You can change the accent color by setting the `accent_color` option in
`conf.py`, for example::

    html_theme_options = {
        'accent_color': '#e74c3c'
    }

.. highlight:: html

You can also hide various elements, for example the nav menu on the left if you
don't plan to have any pages. This can be done by creating a ``page.html`` file
under your blog's ``_templates`` directory with the following content::

    {% extends "!page.html" %}

    {% block navigation %}{% endblock %}

Add a custom stylesheet
-----------------------

.. highlight:: html

Create your own ``style.css`` (filename is not important) and place it under
the blog's ``_static`` directory and create a new ``page.html`` file under
your blog's ``_templates`` directory with the following content::

    {% extends "!page.html" %}

    {% set css_files = css_files + ["_static/style.css"] %}

More information on extending templates can be found
`here <http://sphinx.pocoo.org/templating.html#css_files>`_.

This will apply your stylesheet on top of the styles of the theme you are
using. This way you can easily tweak an existing theme.

Create your own theme
---------------------

Tinkerer uses Sphinx under the hood so its themes are also based on Jinja2 and
somewhat similar to Sphinx, though due to the inherent differences between
documentation and blogs, Sphinx themes are not fully compatible with Tinkerer.
That said, you can still learn the basics from the Sphinx documentation on
`Creating themes <http://sphinx.pocoo.org/theming.html#creating-themes>`_.

Place your new theme in a directory under ``/_themes``. For example,
``_themes/my_awesome_theme`` directory relative to your blog root.

Your theme should contain, at the least, a ``theme.conf`` file, as described by
Sphinx documentation.

You will probably also want to add at least a custom CSS file in its ``static``
subdirectory and maybe extend some boilerplate templates.

To understand how this works, take a peek at the sources of other
`Tinkerer themes <https://github.com/vladris/tinkerer/tree/master/tinkerer/themes>`_.

Tinkerer boilerplate theme
--------------------------

Tinkerer boilerplate theme consist of the following templates:

``layout.html``

    This is the most complex template and defines the general layout of a blog
    web page. It is a merge between the base Sphinx ``layout.html`` and an
    HTML5 Boilerplate page plus Tinkerer additions.

``page.html``

    This extends the ``layout.html`` template and represents a blog post or
    page (it is an extension of a Sphinx page).

``aggregated.html``

    This template represents a page containing multiple aggregated posts, for
    example the homepage of a blog and subsequent pages, each containing a
    number of posts.

``archive.html``

    The template represents a list of posts (just titles and metadata), like
    )he post archive or posts in a particular category, etc.

``rss.html``

    This is the template for the RSS feed (and should probably be left alone).

``search.html``

    Search results page (when using search box).

Besides these, there are also a number of sidebar widgets (``categories.html``,
``tags.html``, ``tags_cloud.html``, ``recent.html``, ``searchbox.html``).

Boilerplate theme style is based on HTML5 boilerplate. You also get the awesome
Web Symbols font included by default, which Tinkerer uses for its RSS symbol
but which also contains a number of other popular symbols you can use.

Back to :ref:`tinkerer_reference`.

