'''
    author
    ~~~~~~

    Post author extension.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
from sphinx.util.compat import Directive
import tinkerer.utils


# author directive
class AuthorDirective(Directive):
    required_arguments = 0
    optional_arguments = 100
    has_content = False

    def run(self):
        env = self.state.document.settings.env

        # store author in metadata
        author = " ".join(self.arguments)
        if author == "default":
            author = env.config.author 
        env.blog_metadata[env.docname].author = author

        return []


