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

    # Change this to the description of your blog
    description = 'This is an awesome blog'

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

**description**

    This will be added to the ``description`` meta tag of your blog pages and
    will be consumed by search engines crawling your blog.

**author**

    Your name.

**copyright**

    The copyright string is displayed at the bottom of each page.

**website**

    The RSS feed requires the address of the website to properly link articles.    

Create a post
~~~~~~~~~~~~~

.. highlight:: bash

From your blog root directory, call::

    tinker --post 'Hello World!'

.. highlight:: rst

Tinkerer will let you know where the file was created. You can edit it right 
away, using reStructuredText! Read more about :ref:`posts`.

Create a page
~~~~~~~~~~~~~

.. highlight:: bash

Create an *About* page to tell your readers about yourself. From your blog 
root directory, call::

    tinker --page 'About'
    
Tinkerer will let you know where the file was created. Read more about 
:ref:`pages`.

Build your blog
~~~~~~~~~~~~~~~

From your blog root directory call::

    tinker --build

Open the ``index.html`` file in your blog's root to preview your blog. Read 
more about :ref:`build`.

.. _tinkerer_reference:

Tinkerer Reference
------------------

.. toctree::
    :maxdepth: 2

    ../doc/tinkering
    ../doc/more_tinkering
    ../doc/deploying
    ../doc/command_line 
    ../doc/internals
    ../doc/theming
    ../doc/extensions
