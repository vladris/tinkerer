Tinkering
=========

Overview
--------

Tinkerer uses `Sphinx <http://sphinx.pocoo.org/>`_ to generate your blog. 
The ``conf.py`` file is a Sphinx project configuration file extended with 
Tinkerer settings. Similarly, the directories (``_static``, ``_templates``
etc.) and the master document (``master.rst``) are part of a standard Sphinx
project.

The logic to extract the post metadata and build the blog pages is implemented
as a Sphinx extension (``tinkerer.ext.blog``). Since your blog is in fact a
Sphinx project, all tinkering enabled by Sphinx will work on your blog too.

The Tinkerer command line is just facilitating authoring and build - for 
example creating a new post requires creating a path for the current date as
``$(YEAR)/$(MONTH)/$(DAY)``, creating the post file, populating the file with
the Tinkerer directives and inserting it in the master document. Tinkerer
command line takes care of all of these steps. For build, the destination
directory is cleaned up and Sphinx build is invoked.

Tinkerer command line should be run from your blog's root (the directory 
containing the ``conf.py`` file), except when setting up a new blog.

.. _posts:

Posts
-----
.. highlight:: bash

From your blog root directory, call::

    tinker --post 'Hello World!'

.. highlight:: rst

A new post will be created and inserted at the top of the TOC in 
``master.rst``. Tinkerer will let you know where the file was created (path is 
based on current date and filename is normalized). Your post file looks like 
this::

    Hello World!
    ============

    .. author:: default
    .. categories:: none
    .. tags:: none
    .. comments::
   
Add content below the title.

**author**

    If left to ``default``, Tinkerer will use the author specified in 
    ``conf.py``. For collaborative blogs, this can be replaced with any string
    containing the name of the author.

**categories**

    Specify a comma-separated list of categories under which the post will be
    filed.    

**tags**

    Specify a comma-separated list of tags for the post.

**comments**

    This tells Tinkerer comments are enabled for this post. Remove the 
    directive to disable posts.
    
**more**

    At any point in your text, you can insert the ``more`` directive::

        Hello World!
        ============

        Some text.

        .. more::

        More text.

    This tells Tinkerer to insert a "Read more..." link into the blog post.
    A "Read more..." link will appear on the front page and the text after the
    directive will be hidden. The full text will be displayed only on the page 
    of the post.
   
.. _pages:
    
Pages
-----

.. highlight:: bash

From your blog root directory, call::

    tinker --page 'About'

.. highlight:: rst

A new page named ``About`` will be created as ``pages/about.rst`` and inserted 
at the bottom of the TOC in ``master.rst`` (pages are always placed under the
``pages`` directory, filename is normalized). Your page file looks like this::

    About
    =====

Unlike posts, pages do not have metadata associated with them. Pages are added 
to the top navigation bar in the order in which they were created. Pages do not
display `previous` and `next` navigation links.

.. _drafts:

Drafts
------

.. highlight:: bash

From your blog root directory, call::

    tinker --draft 'Hello World!'

A new draft named ``Hello World!`` will be created under the ``drafts`` 
directory as ``hello_world_.rst`` (filename is normalized). The content of the 
file is identical to a post file but unlike posts, the draft will not be added 
to the TOC in ``master.rst`` file and will be ignored by the build. You can 
take your time to edit it. When it's ready, from your blog root directory 
call::

    tinker --post drafts/hello_world_.rst

This will promote your draft to a post by moving it to the appropriate
``$(YEAR)/$(MONTH)/$(DAY)`` path and adding it to the TOC in ``master.rst``.

If you change your mind and want to tinker with it some more, from your blog
root directory call::

    tinker --draft 2011/12/25/hello_world_.rst

This will demote your post to a draft by moving it to the ``drafts`` directory
and removing it from the TOC in ``master.rst``.    

.. _build:

Build
-----

From your blog root directory, call::

    tinker --build

Your blog will be generated under ``blog/html``.

Generated pages
~~~~~~~~~~~~~~~

The Sphinx build will convert all the RST documents of your blog to HTML pages.
Besides these, Tinkerer will also generate the following:

**index.html**
    The page will contain the latest 10 posts of your blog with titles hyperlinked
    to the post pages.

**page*.html**
    After the latest 10 posts, all other posts grouped by 10 will be written to
    ``page2.html``, ``page3.html`` and so on.

**categories/***
    For each category posts were filed under, Tinkerer will generate a page under
    the ``categories`` directory, hyperlinking all instances of the category to it.

**tags/***
    Like categories above, Tinkerer will generate similar pages and hyperlinks for
    tags.

**archive.html**
    Additionally, Tinkerer will generate a blog archive containing all posts 
    grouped by publishing year and ordered by publishing date as ``archive.html``.

**rss.html**
    An RSS feed will be generated as ``rss.html``.


Back to :ref:`tinkerer_reference`.
