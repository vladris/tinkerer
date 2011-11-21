'''
    blog
    ~~~~

    Blog extension.

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import metadata
import tags
import rss


# setup extension
def setup(app):
    metadata.setup(app)
    tags.setup(app)
    rss.setup(app)
