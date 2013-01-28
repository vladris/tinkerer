# -*- coding: utf-8 -*-
"""

    pygments shell-session lexer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Pygments lexer for shell session.

    Why: The default '.. sourcecode:: console' directive will highlight
         every line that starts with '#', '$', '>' or 'user@linuxbox'.

         This lexer will highlight:

         [user@host dir]$ ls test
         user@host ~ $ ls test
         user@host:~# ls test

         and not lines starting with '#', '>' or '$'.

    How to use:

      .. sourcecode:: shell-session

        [user@linuxbox ~]$ rpm -ql python-pygments |grep lexers/other
        /usr/lib/python2.7/site-packages/pygments/lexers/other.py
        /usr/lib/python2.7/site-packages/pygments/lexers/other.pyc
        /usr/lib/python2.7/site-packages/pygments/lexers/other.pyo
        [user@linuxbox ~]$

    :copyright: Copyright 2006-2010 by the Pygments team, see
                https://bitbucket.org/birkenfeld/pygments-main/src/default/AUTHORS.
    :copyright: Copyright 2013 by Christian Jann.
    :license: BSD

"""

import re
from pygments.lexer import Lexer, do_insertions
from pygments.lexers.other import BashLexer
from pygments.token import Generic

line_re  = re.compile('.*?\n')

class ShellSessionLexer(Lexer):
    """
    Lexer for shell sessions.
    """

    name = 'Shell Session'
    aliases = ['shell-session']
    filenames = ['*.sh-session']
    mimetypes = ['application/x-shell-session']

    def get_tokens_unprocessed(self, text):
        bashlexer = BashLexer(**self.options)

        pos = 0
        curcode = ''
        insertions = []

        for match in line_re.finditer(text):
            line = match.group()

            # http://rubular.com/ online regular expression editor
            # original: ^((?:|sh\S*?|\w+\S+[@:]\S+(?:\s+\S+)?|\[\S+[@:][^\n]+\].+)[$#%])(.*\n?)
            m = re.match(r'^((?:\[?\S+@[^$#%]+)[$#%])(.*\n?)', line)
            if m:
                # To support output lexers (say diff output), the output
                # needs to be broken by prompts whenever the output lexer
                # changes.
                if not insertions:
                    pos = match.start()

                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, m.group(1))]))
                curcode += m.group(2)
            else:
                if insertions:
                    toks = bashlexer.get_tokens_unprocessed(curcode)
                    for i, t, v in do_insertions(insertions, toks):
                        yield pos+i, t, v
                yield match.start(), Generic.Output, line
                insertions = []
                curcode = ''
        if insertions:
            for i, t, v in do_insertions(insertions,
                                         bashlexer.get_tokens_unprocessed(curcode)):
                yield pos+i, t, v


def setup(app):
    app.add_lexer("shell-session", ShellSessionLexer())
 
