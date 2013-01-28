Creating Custom Extensions
==========================

Custom extension are usually Python scripts that you can add in the ``_exts``
subdirectory of your blog and hook up to the build by updating the
``extensions`` list in your ``conf.py``.

Tinkerer extensions are pretty much Sphinx extensions, so you can start by
reading about `Sphinx extensions <http://sphinx-doc.org/extensions.html>`_.

What Tinkerer adds to this is a set of metadata and other information which is
passed to the templating engine when rendering each file. This information
resides in the :ref:`context` variable and your extensions can use and/or alter it
to extend Tinkerer functionality.

Going forward, the Tinkerer post and page RST templates can be found in the
``_templates`` subdirectory of a blog, so if your custom extension adds, for
example, an additional directive which should appear in each new post, you can
instruct the user to update his post template accordingly (or have a setup 
script that does it automatically).

.. _context:

Context
-------

The context object passed by the builder to the templating engine contains some
additional information added by Tinkerer besides the information provided by
Sphinx. It contains the following extra keys:

``website``, ``tagline``, ``description``

    These are values retrieved from ``conf.py``.

``text_recent_posts``, ``text_posted_by``, ``text_blog_archive``,
``text_filed_under``, ``text_tags``, ``text_tags_cloud``,
``text_categories``

    These are localized strings which are translated by Tinkerer and get passed
    to the templating engine for rendering.

``pages``

    The list of pages (documents under ``/pages``).

``recent``

    The list of recent posts.

``tags``, ``taglinks``, ``categories``, ``catlinks``

    These are the lists of post tags, tag links, categories and category links.

``prev``, ``next``
    
    Previous and next links. These exist only for posts and for documentation
    pages (pages under ``doc/`` directory). Other pages, for example pages
    under ``pages/`` directory, don't have previous/next relationships.

``Metadata``

    This is an object containig additional metadata:

    ``is_post``, ``is_page``

        Flags used to indicate whether what is currently being rendered is a
        post or a page.

    ``title``, ``link``

        Post or page title and link (URL).

    ``date``, ``formatted_date``, ``formatted_date_short``

        Post timestamp. ``date`` is raw date; ``formatted_date`` is date
        formatted as string using localized formatting; 
        ``formatted_date_short`` is similar to ``formatted_date`` but using a
        short format (month and day, without year).
    
    ``body``

        HTML body of the post as converted from RST.

    ``author``
        
        Post author.

    ``filing``

        Filing dictionary which contains two keys: ``tags`` and ``categories``.
        These contain the list of tags and categories of the post.

    ``comments``

        ``True`` if post should display a comment box.

    ``comment_count``
    
        Contains additional HTML/JavaScript code to retrieve the number of
        comments of a post. Extensions like the built-in *disqus* or
        *fbcomments* populate this value.

    ``num``

        This is a number which will be unique for each post during a build. It
        can be used to associate data with posts.

Back to :ref:`tinkerer_reference`.

