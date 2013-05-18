Add Extra Jinja Filters
=======================
.. highlight:: python

This is an example how to add custom Jinja filters to Sphinx's
HTML builder.

Example: ::

  def add_jinja_filters(app):
      app.builder.templates.environment.filters['cleanurl'] = name_from_title

  def setup(app):
      '''
      Adds extra jinja filters.
      '''
      app.connect("builder-inited", add_jinja_filters)

Now ``{{ "This is a title"|cleanurl }}`` will be replaced with ``this_is_a_title``.


This could be an alternative to:
``catlinks = sorted([(c, name_from_title(c)) for c in env.filing["categories"]])``.
We could just use ``{{ category|cleanurl }}`` instead of ``{{ catlinks[category]) }}``
(http://comments.gmane.org/gmane.comp.python.sphinx.devel/6137).
