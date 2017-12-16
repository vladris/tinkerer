'''
    readmore
    ~~~~~~~~

    Read more directive.

    :copyright: Copyright 2012 by Christian Jann
    :copyright: Copyright 2011-2018 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from docutils import nodes
from docutils.parsers.rst import Directive


class InsertReadMoreLink(Directive):
    '''
    Sphinx extension for inserting a "Read more..." link.
    '''

    has_content = True
    required_arguments = 0

    def run(self):
        return [nodes.raw("", '<div id="more"> </div>', format="html")]
