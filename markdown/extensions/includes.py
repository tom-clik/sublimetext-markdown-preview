"""
# Allow includes for Python-Markdown


Basic Usage:

    [include file="otherfile.md"]

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
INCLUDE_RE = re.compile(r'\[include\s+file\s*\=[\"\']{,1}(?P<filename>.*?)[\"\']{,1}\s*\]')

class IncludesExtension (Extension):
    """ Alphaeta-Data extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add IncludesPreprocessor to Markdown instance. """

        md.preprocessors.add("includes", IncludesPreprocessor(md), "_begin")


class IncludesPreprocessor(Preprocessor):
    """ Get Meta-Data. """

    def run(self, lines):
        """ Parse includes """
        meta = {}
        key = None
        text = "\n".join(lines)

        base_url = None
        if self.markdown.Meta:
            if "base_url" in self.markdown.Meta:
                base_url = self.markdown.Meta

        m1 = INCLUDE_RE.search(text)
        #print(m1)

        while m1:
          
            filename = m1.group('filename').strip()
            if base_url:
                filename = self.markdown.Meta['base_url'] + filename
            f = open(filename,'r', encoding='utf-8')
            includetext = f.read()
            f.close()

            matchStr = text[m1.start():m1.end()]
            #print(matchStr)
            text = text.replace(matchStr,includetext)

            m1 = INCLUDE_RE.search(text)

        return text.split("\n")
        
def makeExtension(configs={}):
    return IncludesExtension(configs=configs)
