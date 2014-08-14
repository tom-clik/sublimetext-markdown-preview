"""
Quick QuickTable Extension for Python-Markdown
=============================================

Added parsing of Definition List like QuickTables to Python-Markdown.

A simple example:

    -Term 1         A definition
    -Term 2         Another definition

Copyright 2014 - Tom Peer

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..blockprocessors import BlockProcessor
from ..util import etree

import re
#import pprint

class QuickTableProcessor(BlockProcessor):

    QUICK_RE = re.compile('^\-\W*(?P<def>.*?)( {4,}|\t+)(?P<term>.*)$')
    
    def test(self, parent, block):
        rows = block.split('\n')
        return (len(rows) >= 2 and
                self.QUICK_RE.match(rows[0])
                    )
        
    def run(self, parent, blocks):
        """ Parse a QuickTable block and build QuickTable. """
        block = blocks.pop(0).split('\n')
        
        # Build QuickTable
        quickTable = etree.SubElement(parent, 'table')
        
        for row in block:
            print(row)
            m = self.QUICK_RE.match(row)
            if m: 
                print(m.group('def'), m.group('term'))
                tr = etree.SubElement(quickTable, 'tr')
                c = etree.SubElement(tr, 'td')
                c.text = m.group('def')
                d = etree.SubElement(tr, 'td')
                d.text = m.group('term')
            else:
                print('no match')

class QuickTableExtension(Extension):
    """ Add QuickTables to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of QuickTableProcessor to BlockParser. """
        md.parser.blockprocessors.add('QuickTable', 
                                      QuickTableProcessor(md.parser),
                                      '<hashheader')

def makeExtension(configs={}):
    return QuickTableExtension(configs=configs)

