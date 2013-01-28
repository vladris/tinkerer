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

Back to :ref:`tinkerer_reference`.

