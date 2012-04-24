'''
    readmore
    ~~~~~~~~

    Read more directive.

    :copyright: Copyright 2012 by Christian Jann
    :license: FreeBSD, see LICENSE file
'''
from docutils import nodes
from sphinx.util.compat import Directive



class InsertReadMoreLink(Directive):
    '''
    Sphinx extension for inserting a "Read more..." link.
    '''

    has_content = True
    required_arguments = 0


    def run(self):
        return [nodes.raw("", "<!-- more -->", format="html")] 

