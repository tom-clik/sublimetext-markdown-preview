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

    ::warning:: Danger
        Be careful when doing this

A floating image

    ::imageboxleft::
            [Alt text](http://images.com/image.jpg)
            
            caption:
                Image caption

Outputs:
    <p class="intro">The introduction paragraph here</p>

    <div class="warning"><p class="warning-title">Danger</p><p>Be careful when doing this</p></div>

     <div class="imageboxleft"><image src="http://images.com/image.jpg" /><p class="caption">Image caption</p></div>

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

    RE = re.compile(r'(?:^|\n)\:{1,2}([\w\-]+):{1,2}\s+(.*?)$')

    def test(self, parent, block):
        sibling = self.lastChild(parent)
        return self.RE.search(block) or \
            (block.startswith(' ' * self.tab_length) and sibling)

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            block = block[m.end() + 1:]  # removes the first line

        block, theRest = self.detab(block)

        if m:
            klass, title = self.get_class_and_title(m)
            div = etree.SubElement(parent, 'div')
            div.set('class', '%s %s' % (self.CLASSNAME, klass))
            if title:
                p = etree.SubElement(div, 'p')
                p.text = title
                p.set('class', self.CLASSNAME_TITLE)
        else:
            div = sibling

        self.parser.parseChunk(div, block)
        
        if theRest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, theRest)

    def get_class_and_title(self, match):
        klass, title = match.group(1).lower(), match.group(2)
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
