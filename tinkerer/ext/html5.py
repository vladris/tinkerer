"""
    html5
    ~~~~~

    Monkey-patch Sphinx HTML translator to emit HTML5.

    :copyright: Copyright 2011-2015 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file.
"""
from sphinx.writers.html import HTMLTranslator


def visit_desc_addname(self, node):
    '''
    Similar to Sphinx but using a <span> node instead of <tt>.
    '''
    self.body.append(self.starttag(node, 'span', '', CLASS='descclassname'))


def depart_desc_addname(self, node):
    '''
    Similar to Sphinx but using a <span> node instead of <tt>.
    '''
    self.body.append('</span>')


def visit_desc_name(self, node):
    '''
    Similar to Sphinx but using a <span> node instead of <tt>.
    '''
    self.body.append(self.starttag(node, 'span', '', CLASS='descname'))


def depart_desc_name(self, node):
    '''
    Similar to Sphinx but using a <span> node instead of <tt>.
    '''
    self.body.append('</span>')

def patch_translator():
    '''
    Monkey-patch Sphinx translator to emit proper HTML5.
    '''
    HTMLTranslator.visit_desc_addname = visit_desc_addname
    HTMLTranslator.depart_desc_addname = depart_desc_addname
    HTMLTranslator.visit_desc_name = visit_desc_name
    HTMLTranslator.depart_desc_name = depart_desc_name
