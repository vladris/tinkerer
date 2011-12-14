Documentation
=============

Getting Started
---------------

Setup
~~~~~

.. highlight:: bash

After you installed the Tinkerer package, create your blog directory and cd
into it::

    mkdir myblog
    cd myblog

Run Tinkerer setup::

    tinker --setup
   
.. highlight:: python   
    
There is some minimal configuration required in ``conf.py``::

    # Change this to the name of your blog
    project = 'My blog'                   

    # Change this to the tagline of your blog
    tagline = 'Add intelligent tagline here'                  

    # Change this to your name
    author = 'Winston Smith'

    # Change this to your copyright string
    copyright = '1984, ' + author         

    # Change this to your blog root URL (required for RSS feed)
    website = 'http://127.0.0.1/blog/html/'                              
 
**project**

    This will be the name of your blog.

**tagline**

    The tagline is displayed right after the name of the blog and as the blog
    description in the RSS feed.

**author**

    Your name.

**copyright**

    The copyright string is displayed at the bottom of each page.

**website**

    The RSS feed requires the address of the website to properly link articles.    

Create a post
~~~~~~~~~~~~~

.. highlight:: bash

From your blog directory root, call::

    tinker --post 'Hello World!'

.. highlight:: rst

Tinkerer will let you know where the file was created (path is based on current
date and filename is normalized). Your post file looks like this::

    Hello World!
    ============



    .. author:: default
    .. categories:: none
    .. tags:: none
    .. comments::

Add content below the title.

**author**

    If left to ``default``, Tinkerer will use the author specified in 
    ``conf.py``. For colaborative blogs, this can be replaced with any string
    containing the name of the author.

**categories**

    Specify a comma-separated list of categories under which the post will be
    filed.    

**tags**

    Specify a comma-separated list of tags for the post.

**comments**

    This tells Tinkerer comments are enabled for this post. Remove the 
    directive to disable posts.

Create a page
~~~~~~~~~~~~~

.. highlight:: bash

Create an *About* page to tell your readers about yourself. From your blog 
directory root, call::

    tinker --page 'About'
    
Tinkerer will let you know where the file was created (path is under ``/pages``
and filename is normalize).    

.. highlight:: rst

Pages are added to the top navigation bar in the order in which they were 
created. Your page file looks like this::

    About
    =====

Pages do not have post metadata associated with them (author, categories, tags,
comments).    

Build your blog
~~~~~~~~~~~~~~~

From your blog directory root call::

    tinker --build

Your blog will be generated under ``./blog/html``.    

.. _tinkerer_reference:

Tinkerer Reference
==================

.. toctree::
    ../doc/tinkering
    ../doc/deploying
    ../doc/command_line 
    ../doc/internals

    
