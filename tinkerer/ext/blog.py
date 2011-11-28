'''
    blog
    ~~~~

    Blog extension.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import tinkerer.ext.author
import tinkerer.ext.metadata
import tinkerer.ext.tags
import tinkerer.ext.rss


# setup extension
def setup(app):
    tinkerer.ext.author.setup(app)
    tinkerer.ext.metadata.setup(app)
    tinkerer.ext.tags.setup(app)
    tinkerer.ext.rss.setup(app)
