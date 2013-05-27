Facebook Comments
=================
.. highlight:: python

As an alternative to Disqus comments, you can use Facebook Comments on your
blog. To enable Facebook comments, download ``fbcomments.py`` in your blog's
``_exts`` directory and replace the default ``tinkerer.ext.disqus`` extension
in ``conf.py`` with ``fbcomments``::

    # Add other Sphinx extensions here
    extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus']

should become::

    # Add other Sphinx extensions here
    extensions = ['tinkerer.ext.blog', 'fbcomments']

Blog posts don't need to change as this extension is a different handler for
the same ``comments`` directive.

The above steps enable the Facebook Comment Box. More information on this in
the `Facebook Developers Documentation <https://developers.facebook.com/docs/reference/plugins/comments/>`_.

There are two options for managing comments: using a user ID or an app ID.

.. highlight:: html

User Admin
----------

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

You will also have to copy the ``fb.js`` file supplied with this extension to
your blog's ``_static`` directory.

App Admin
---------

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

