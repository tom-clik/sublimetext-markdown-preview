"""
# Alpha Meta Data Extension for Python-Markdown

This extension adds @Meta Data handling to markdown.

Basic Usage:

    >>> import markdown
    >>> text = '''@Title    A Test Doc.
    ...
    ... The body. This is paragraph one.
    ... '''
    >>> md = markdown.Markdown(['alphameta'])
    >>> print md.convert(text)
    <p>The body. This is paragraph one.</p>
    >>> print md.Meta
    

Copyright 2007-2008 [Waylan Limberg](http://achinghead.com).

Project website: <http://packages.python.org/Markdown/meta_data.html>
Contact: markdown@freewisdom.org

License: BSD (see ../LICENSE.md for details)

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..preprocessors import Preprocessor
import re

# Global Vars
META_RE = re.compile(r'^\@(?P<key>[A-Za-z0-9_-]+)\s+(?P<value>.*)')

class AlphametaExtension (Extension):
    """ Alphaeta-Data extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add AlphametaPreprocessor to Markdown instance. """

        md.preprocessors.add("alphameta", AlphametaPreprocessor(md), "_begin")


class AlphametaPreprocessor(Preprocessor):
    """ Get Meta-Data. """

    def run(self, lines):
        """ Parse Meta-Data and store in Markdown.Meta. """
        meta = {}
        key = None
        while lines:
            line = lines.pop(0)
            # if line.strip() == '':
                #break # blank line - done
            m1 = META_RE.match(line)
            if m1:
                key = m1.group('key').lower().strip()
                value = m1.group('value').strip()
                try:
                    meta[key].append(value)
                except KeyError:
                    meta[key] = [value]
            """ else:
                m2 = META_MORE_RE.match(line)
                if m2 and key:
                    # Add another line to existing key
                    meta[key].append(m2.group('value').strip())
                else:
                    lines.insert(0, line)
                    break # no meta data - done """
        self.markdown.Meta = meta
        return lines
        
def makeExtension(configs={}):
    return AlphametaExtension(configs=configs)
