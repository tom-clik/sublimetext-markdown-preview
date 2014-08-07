"""
Tables Extension for Python-Markdown
====================================

Added parsing of tables to Python-Markdown.

A simple example:

    First Header  | Second Header
    ------------- | -------------
    Content Cell  | Content Cell
    Content Cell  | Content Cell

Copyright 2009 - [Waylan Limberg](http://achinghead.com)

Updated  by Tom Peer

1. Header row is now optional. Just start with separator row
2. Double dividers with no content are colspans. NB no spaces. NB Also no ending rows with doubles -- just omit the cells to span the rest
3. Cells with FOUR or more dashes are row spans
4. Any cell can have its own alignment

A complex example 

    ------------- | ------------- | --------------
    Row span      | col span                      
    ----          | Content Cell  |: center      :|

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..blockprocessors import BlockProcessor
from ..util import etree

import re
#import pprint

class TableProcessor(BlockProcessor):

    SEPERATOR = re.compile('^[\W\-\:\|]+$')
    #pattern to indicate rowspan -- at least 4 dashes
    ROWSPAN = re.compile('^\W*\-{4,}\W*$')

    def test(self, parent, block):
        p = re.compile('^[\W\-\:]+$')
        rows = block.split('\n')
        return (len(rows) >= 2 and '|' in rows[0] and 
                '|' in rows[1] and (
                    self.SEPERATOR.match(rows[0]) or self.SEPERATOR.match(rows[1]))
                    )
        
    def run(self, parent, blocks):
        """ Parse a table block and build table. """
        block = blocks.pop(0).split('\n')
        
        hasheaderRow = 0
        if self.SEPERATOR.match(block[1]):
             hasheaderRow = 1
             blockstart = 2
             seperator  = block[1].strip()
             header = block[0].strip()

        else:
            blockstart = 1
            seperator  = block[0].strip()
                
        rows = block[blockstart:]

        # Get format type (bordered by pipes or not)
        border = False
        if seperator.startswith('|'):
            border = True
        # Get alignment of columns
        align = []
        for c in self._split_row(seperator, border):
            align.append(self._get_alignment(c))
        # Build table
        table = etree.SubElement(parent, 'table')
        if hasheaderRow:
            thead = etree.SubElement(table, 'thead')
            cells = self._split_row(header, border)
            self._build_row(header, thead, align, border)

        tabledata = {}
        rownum = 0

        for row in rows:
            colnum = 0
            cells = self._split_row(row, border)
            
            # build struct of structs keyed by rownum and colnum.
            tabledata[rownum] = {}
            for cell in cells:
                
                cellalign = self._get_alignment(cell)
                cell = cell.strip(":")
                cell = cell.strip()
                colspan = 1
                rowspan = 1
                celldisplay = True
                
                #completely blank cell indicates colspan
                if cell == "":
                    if colnum > 0:
                         tabledata[rownum][colnum -1]['colspan'] += 1
                         celldisplay = False
                    else:
                        cell = "&nbsp;"

                #Cell with just hyphens indicates rowspan
                if self.ROWSPAN.match(cell):
                    if rownum > 0:
                         tabledata[rownum -1][colnum]['rowspan'] += 1
                         celldisplay = False
                    else:
                        cell = "&nbsp;"

                if not cellalign:
                    if len(align) < colnum:
                        raise Exception('row ' + row + ' has more columns than header')
                    cellalign = align[colnum -1]

                tabledata[rownum][colnum] = {'text' : cell,'align':cellalign,'display' : celldisplay,'colspan' : colspan,'rowspan' : rowspan}

                colnum +=1
            
            # check we had all cols otherwise add colspan to last cell of row
            print ('colnum is ' +str(colnum) + ' align is ' + str(len(align)))
            if len(align) > colnum:
                tabledata[rownum][colnum-1]['colspan'] += len(align) - colnum

            rownum += 1
        
        tbody = etree.SubElement(table, 'tbody')
        
        for row in tabledata:
            tr = etree.SubElement(tbody, 'tr')
            for col in tabledata[row]:
                 cell = tabledata[row][col]
                 if cell['display']:
                    c = etree.SubElement(tr, 'td')
                    c.text = cell['text']
                    if cell['align']:
                        c.set('align',cell['align'])
                    if cell['rowspan'] > 1:
                        c.set('rowspan',str(cell['rowspan']))
                    if cell['colspan'] > 1:
                        c.set('colspan',str(cell['colspan']))
    
    def _get_alignment(self,cell):
        """ Get the alignment of a cell from the colon format """
        align = None
        if cell.startswith(':') and cell.endswith(':'):
            align ='center'
        elif cell.startswith(':'):
            align ='left'
        elif cell.endswith(':'):
            align ='right'
        return align      
    
    def _build_row(self, row, parent, align, border):
        """ Given a row of text, build table cells. """
        tr = etree.SubElement(parent, 'tr')
        tag = 'td'
        if parent.tag == 'thead':
            tag = 'th'
        cells = self._split_row(row, border)
        # We use align here rather than cells to ensure every row 
        # contains the same number of columns.
        for i, a in enumerate(align):
            c = etree.SubElement(tr, tag)
            try:
                c.text = cells[i].strip()
            except IndexError:
                c.text = ""
            if a:
                c.set('align', a)
    
    def _split_row(self, row, border):
        """ split a row of text into list of cells. """
        if border:
            if row.startswith('|'):
                row = row[1:]
            if row.endswith('|'):
                row = row[:-1]
        return row.split('|')


class TableExtension(Extension):
    """ Add tables to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of TableProcessor to BlockParser. """
        md.parser.blockprocessors.add('table', 
                                      TableProcessor(md.parser),
                                      '<hashheader')

def makeExtension(configs={}):
    return TableExtension(configs=configs)
