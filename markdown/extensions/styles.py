"""
# Styles extension for Python-Markdown

Allow for paragraph styling using reStructured text-like syntax. We have to start with colons as well though to avoid conflict with meta

A single lower case class name followed by a colon will assign that classname to the following paragraph

A colon, a single lower case class name followed by a double colon and optionally a title will create a div
with that classname, the title in a para of style (stylename)-title, and place the following paras in it.

A simple example:
    :intro:
        The introduction paragraph here

A generic Styles style

    :warning:: 
        ## Danger

        Be careful when doing this

A floating image

    ::imageboxleft::
            
            ![Alt text](http://images.com/image.jpg)
            
            ::caption::
                Image caption

Outputs:
    <p class="intro">The introduction paragraph here</p>

    <div class="warning"><h2>Danger</h2><p>Be careful when doing this</p></div>

     <div class="imageboxleft"><image src="http://images.com/image.jpg" /><div class="caption">Image caption</div></div>

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..blockprocessors import BlockProcessor
from ..util import etree
import re

class StylesExtension(Extension):
    """ Styles extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add Styles to Markdown instance. """
        md.registerExtension(self)

        md.parser.blockprocessors.add('Styles',
                                      StylesProcessor(md.parser),
                                      '_begin')


class StylesProcessor(BlockProcessor):

    #RE = re.compile(r'(?:^|\n)\:{1,2}([\w\-]+):{1,2}\s+(.*?)$')
    RE = re.compile(r'(?:^|\n)\:{1,2}([\w\-]+)\:{1,2}')

    def test(self, parent, block):
        sibling = self.lastChild(parent)
        if self.RE.search(block) or \
            (block.startswith(' ' * self.tab_length) and sibling):
            print('Ok')
            return True
        else:
            print('didnt match')
            return False
         

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            block = block[m.end() + 1:]  # removes the first line

        block, theRest = self.detab(block)

        if m:
            klass = m.group(1).lower()
            div = etree.SubElement(parent, 'div')
            div.set('class', klass)
            
        else:
            div = sibling

        self.parser.parseChunk(div, block)
        
        if theRest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, theRest)

    def get_class_and_title(self, match):
        klass = match.group(1).lower()
        if title is None:
            # no title was provided, use the capitalized classname as title
            # e.g.: `!!! note` will render `<p class="Styles-title">Note</p>`
            title = klass.capitalize()
        elif title == '':
            # an explicit blank title should not be rendered
            # e.g.: `!!! warning ""` will *not* render `p` with a title
            title = None
        return klass, title


def makeExtension(configs={}):
    return StylesExtension(configs=configs)
