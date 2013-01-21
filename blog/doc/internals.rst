Internals
=========

The master document
-------------------

Sphinx requires a master document that contains the table of contents and
establishes the relationship between all other documents. Tinkerer sets this
up as the root ``master.rst`` document. More information on the `Table of 
Contents <http://sphinx.pocoo.org/concepts.html#the-toc-tree>`_ on the Sphinx 
website.

When creating new posts/pages, tinkerer does not parse the file so it has no
semantic context. Posts are always inserted on the second line after the 
``:maxdepth:`` directive. Pages are always appended at the end of the file
(bottom of the table of contents).

If you are tinkering with this file, make sure not to remove the ``:maxdepth:``
directive and not to insert anything after the table of contents. This will
most likely break Tinkerer posting. You should be able to add content before
the TOC and insert TOC items between the last and first items.

Posts
-----

Tinkerer identifies posts by the document path. If the path to the document is 
of the form ``$(YEAR)/$(MONTH)/$(DAY)``, Tinkerer considers the document to be
a post. The post pubdate is extracted from the path. Additional metadata -
author, categories, tags, comments - is extracted from the post content. Unlike
other documents in the project, posts are archived, filed by category and tag
and aggregated on the front page(s).

Pages
-----

Tinkerer identifies pages by the document path. If the document is under the
``pages`` directory, Tinkerer considers the document to be a page. Unlike other
documents, pages are rendered on the top navigation bar.

Drafts
------

Documents under the ``drafts`` directory are ignored by the build. This 
directory should contain the drafts which are not yet supposed to be published.

Other documents
---------------

Documents which are not identified as either posts or pages are built normally
by Sphinx and Tinkerer will not give them any special treatment. This can be
useful when you want to embed some other documents in your blog. To provide
minimal support for embedding documentation, Tinkerer will display the **prev**
and **next** links at the top of pages placed under ``doc/`` or ``docs/``
directory.

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

