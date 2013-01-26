'''
    author
    ~~~~~~

    Post author extension.

    :copyright: Copyright 2011-2013 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from sphinx.util.compat import Directive
import tinkerer.utils



class AuthorDirective(Directive):
    '''
    Author directive. The directive is not rendered, just stored in the 
    metadata and passed to the templating engine.
    '''
    required_arguments = 0
    optional_arguments = 100
    has_content = False

    def run(self):
        '''
        Called when parsing the document.
        '''
        env = self.state.document.settings.env

        # store author in metadata
        author = " ".join(self.arguments)
        if author == "default":
            author = env.config.author 
        env.blog_metadata[env.docname].author = author

        return []

class AuthorUrlDirective(Directive):
    '''
    Author URL directive. The directive is not rendered, just stored in the
    metadata and passed to the templating engine.
    '''
    required_arguments = 0
    optional_arguments = 100
    has_content = False

    def run(self):
        '''
        Called when parsing the document.
        '''
        env = self.state.document.settings.env

        # store author in metadata
        author_url = " ".join(self.arguments)
        if author_url == "default":
            author_url = env.config.author_url
        env.blog_metadata[env.docname].author_url = author_url

        return []
