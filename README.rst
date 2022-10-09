Announcement
============

Tinkerer is retired in favor of `Baku <https://github.com/vladris/baku>`_.

Tinkerer has been around since 2011 but hasn't been actively developed for
a few years now. The project is using Sphinx for rendering, unfortunately
some of the core functionality required by Tinkerer stopped working in newer
Sphinx versions. The Sphinx dependency has been pinned at version 1.7.1, but
this is quite old and it is no longer working properly with the latest
Python versions.

A lot has changed since 2011. Markdown is now ubiquitous and it supports
some of the content types that used to only work with reStructuredText, like
math, footnotes, and tables. Developing for the web is easier.

`Baku <https://github.com/vladris/baku>`_ takes the learnings from Tinkerer and
provides the same familiar command line interface but uses Markdown for content,
achieves the same look & feel with much lighter HTML/CSS, and fewer
dependencies. It is a modern take on Tinkerer which I hope you try and enjoy.

You can migrate an existing blog using reStructuredText to Markdown by using
`Pandoc <https://pandoc.org/>`_.
