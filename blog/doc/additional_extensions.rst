Additional Extensions
=====================

.. _fb-comments:

Facebook Comments
-----------------
.. highlight:: python

As an alternative to Disqus comments, you can use Facebook Comments on your
blog. To enable Facebook comments, replace the default ``tinkerer.ext.disqus``
extension in ``conf.py`` with ``tinkerer.ext.fbcomments``::

    # Add other Sphinx extensions here
    extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus']

should become::

    # Add other Sphinx extensions here
    extensions = ['tinkerer.ext.blog', 'tinkerer.ext.fbcomments']

Blog posts don't need to change as this extension is a different handler for
the same ``comments`` directive.

The above steps enable the Facebook Comment Box. More information on this in
the `Facebook Developers Documentation <https://developers.facebook.com/docs/reference/plugins/comments/>`_.

There are two options for managing comments: using a user ID or an app ID.

.. highlight:: html

User Admin
~~~~~~~~~~

To enable comment administration, you will need to list yourself as an admin
using a meta tag. You can do this by extending the ``page.html`` template:
create a ``page.html`` file under your blog's ``_templates`` directory with the
following content::

    {% extends "!page.html" %}

    {%- block extrahead %}
        <meta property="fb:admins" content="$(YOUR_FACEBOOK_USER_ID)"/>
        {{ super() }}
    {% endblock %}

Make sure to replace ``$(YOUR_FACEBOOK_USER_ID)`` above with the appropriate
ID.

App Admin
~~~~~~~~~

Facebook recommends to get an application ID so you can manage all comments on
the website in a centralized place. Go to `Facebook Developers Webiste
<https://developers.facebook.com>`_ and create a new application. In your app
settings, make sure to check ``Website`` and update ``Site URL`` with your
blog's URL. Once you have an App ID connected to your website, you no longer
need to list yourself as an administrator, rather you need to provide the App
ID using a meta tag. Create a ``page.html`` under ``_templates`` directory as
above, but with the following content::

    {% extends "!page.html" %}

    {%- block extrahead %}
        <meta property="fb:app_id" content="$(YOUR_APP_ID)"/>
        {{ super() }}
    {% endblock %}

Make sure to replace ``$(YOUR_APP_ID)`` above with the appropriate ID.

.. note::
    Unlike Disqus, Facebook comment box does not inherit the blog theme style.
    Tinkerer will not provide any styling for the comment box.


Using on github pages
---------------------

This extension provides support for github pages.
By default Github pages prohibits names starting with '_'.
But sphinx requires them. It is internal strategy to use '_'
for directory with static content.
To change this behaviour you need to add '.nojekyll' file in a base
direcotry. This extension automates the process.

To use this just add this module to your extensions list in conf.py file, like::

    extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus', 'tinkerer.ext.withhtml']


Using static html pages
-----------------------

If you have some static html pages and don't want to render revrite them
in a rst or something else use this extension.
It provides support for attaching static html pages in your docs dir
To use this just add ``tinkerer.ext.withhtml`` module to your extensions list in conf.py file, like::

    extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus', 'tinkerer.ext.withhtml']

and add your html files to *docs* directory.
Then when tinkerer will build your portal, it will copy all html files
(and render .rst files) from *docs* to *blog/html/docs*.



Back to :ref:`tinkerer_reference`.
