Tinkerer 1.4 Released
=====================

What's New
----------

* New ``--template`` flag that allows using a custom RST template for a given
  post or page
* New ``rss_max_items`` config option to limit the number of RSS items to be
  placed in the feed 
* Tinkerer now uses `Font Awesome <http://fortawesome.github.io/Font-Awesome/>`_
  (also see deprecation warning below)
* Generated HTML now has `WAI-ARIA roles <http://www.w3.org/WAI/intro/aria>`_ 
* Updated Russian localization
* Updated site-search JS script to newer version from Sphinx project
* Other bug fixes and improvements under the hood

Also check out the new :ref:`atomfeed` extension.

Deprecation Warning
-------------------

Until the previous version, Tinkerer shipped with Web Symbols font used for
RSS feed and search button symbols. With this release, Tinkerer moves to use
Font Awesome.

If you are using any other of the Web Symbols glyphs on a modified website (to
render, for example, the Twitter logo), you will need to update your HTML/CSS 
to use the equivalent Font Awesome symbol instead.

Out-of-the-box Tinkerer with no modifications should not be impacted by this
change.

Upgrade Notes
-------------

Tinkerer does some internal HTML processing to patch some tags produced by the
Sphinx build. With this release, Tinkerer moved to use PyQuery to do this which
improves robustness. With this move, Tinkerer now has a dependency on LXML
library which has to be built from source. If you encounter any issues during
upgrade regarding LXML:

On Windows
~~~~~~~~~~

There is a binary distribution of LXML maintained by Christoph Gohlke. You can
download it from `here <http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml>`_.

Download, install, then re-run Tinkerer upgrade.

On Linux
~~~~~~~~

If LXML bulid or link fails, make sure you have the following packages:
``python-dev``, ``libxml2-dev``, ``libxslt-dev`` and ``zlib1g-dev``. Get them
with ``apt-get install python-dev libxml2-dev libxslt-dev zlib1g-dev`` or
equivalent.

Acknowledgments
---------------

Many thanks to `the contributors <https://github.com/vladris/tinkerer/blob/master/CONTRIBUTORS>`_ 
for all the geat work!

.. author:: default
.. categories:: tinkerer
.. tags:: tinkerer, release
.. comments::
