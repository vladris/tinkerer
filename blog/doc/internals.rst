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

Other documents
---------------

Documents which are not identified as either posts or pages are built normally
by Sphinx and Tinkerer will not give them any special treatment. This can be
useful when you want to embed some project documentation on your blog - for 
example the Tinkerer documenation is a set of files under a ``doc`` directory.

Generated pages
---------------

The Sphinx build will convert all the RST documents of your blog to HTML pages.
Besides these, Tinkerer will also generate the following:

index.html
~~~~~~~~~~

The page will contain the latest 10 posts of your blog with titles hyperlinked
to the post pages.

page*.html
~~~~~~~~~~

After the latest 10 posts, all other posts grouped by 10 will be written to
``page2.html``, ``page3.html`` and so on.

categories/*
~~~~~~~~~~~~

For each category posts were filed under, Tinkerer will generate a page under
the ``categories`` directory, hyperlinking all instances of the category to it.

tags/*
~~~~~~

Like categories above, Tinkerer will generate similar pages and hyperlinks for
tags.

archive.html
~~~~~~~~~~~~

Additionally, Tinkerer will generate a blog archive containing all posts 
grouped by publishing year and ordered by publishing date as ``archive.html``.

rss.html
~~~~~~~~

An RSS feed will be generated as ``rss.html``.

Back to :ref:`tinkerer_reference`.

