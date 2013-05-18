Tinkerer 1.1 Released
=====================

What's New
----------

* Tinkerer extension repository at `tinkerer-contrib <https://github.com/vladris/tinkerer-contrib>`_.
* Improved extension mechanism and documentation
* Easier to customize post and page templates for your blog
* Improved HTML5 compliance
* HTML meta description for blogs
* *Minimal5* theme similar to *Minimal* theme but based on HTML5 Boilerplate
* Other bug fixes

Upgrading
---------

Important notes on upgrading:

* Run ``tinkerer --setup`` in your blog root. This will copy ``page.rst`` and
  ``post.rst`` to your blog' ``_templates`` directory. You can customize them
  to tweak your default posts and pages (other contrib extensions can also
  leverage this).
* If you are using ``hidemail`` or ``fbcomments`` extensions, the extensions
  moved to ``tinkerer-contrib``, meaning they no longer come out-of-the-box.
  Please pull them from there and place them in the ``_exts`` subdirectory of
  your blog.
* There is a new ``description`` field you can add to your ``conf.py``, which
  will become an HTML meta description on the generated pages. This appears
  automatically in newly setup blogs but, by design, Tinkerer upgrade does not
  alter existing ``conf.py`` files in any way.

Deprecation Notice
------------------

The old themes not based on HTML5 Boilerplate will be removed in the next
Tinkerer release. These are the *tinkerbase* base theme and the *minimal* and
*modern* themes.

This release brings an alternative *minimal5* theme with a similar look to the
*minimal* theme. The *minimal* theme was built with customization in mind so if
you are using it, please make sure to alter your CSS to support the new
*minimal5* theme. Since *minimal5* has a different base theme, elements
might have different tags/classes/ids.

Acknowledgements
----------------

As usual, many thanks to everyone involved for your suggestions, bug reports
and pull requests!

.. author:: default
.. categories:: tinkerer
.. tags:: tinkerer, release
.. comments::
