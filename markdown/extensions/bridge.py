"""

# Bridge Tag parser for Markdown

Allows PBN bridge markup to be included in Markdown text.

## Usage

Can be used for simple hand holdings (inline or block), suit positions, full deals, auctions, and full bridge diagrams with everything.

## Examples

### A simple hand (inline)

    [bridge]AK952.QJ6.-.QT742[/bridge]

### A simple hand (block)

    [bridge]
    AK952.QJ6.-.QT742
    [/bridge]

### A single suit combo (2 or 4 hands)

    [bridge]AK542 Q97 63 JT8[/bridge]

### A simple auction

    [bridge]
    1C  1S
    2S  3D
    3S  4S
    [/bridge] 

### A full deal
        
    [bridge]
    [Vulnerable "None|All|NS|EW"]
    [Deal "S:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85"]
    [Scoring "IMP"]
    [Declarer "S"]
    [Contract "5HX"]
    [Result "9"]
    [Auction]
    1D 1S 3H =1= 4S
    4NT =2= X Pass Pass
    5C X 5H X
    Pass Pass Pass
    [Note "1:non-forcing 6-9 points, 6-card"]
    [Note "2:two colors: clubs and diamonds"]
    [/bridge]

## Styling the output

hands:

auction:

info:

style:

## Status

Got as far as writing this documentation and copying the footnote extension

Not sure whether I'm going to get away without a block processor. Looking at the detectTabbed function it looks like I may be able just to use something similar.

The plan then is essentially the same: strip out all the tags and replace them with place holders. They we just need to call our tag parser for the content and replace...

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..preprocessors import Preprocessor
import re

class BridgeExtension(Extension):
    """ Bridge Extension. """

    def __init__ (self, configs):
        """ Setup configs. """
        self.config = {'UNIQUE_IDS':
                       [False,
                        "Avoid name collisions across "
                        "multiple calls to reset()."],
                        'VULNERABILTY':{
                            'none':'Love all',
                            'all': 'Game all',
                            'ns': 'NS vulnerable',
                            'ew': 'EW vulnerable',
                        },
                        'SCORING':{
                            'mp': 'Matchpoint scoring',
                            'pab': 'Point a board'
                        }
                       }

        for key, value in configs:
            self.config[key][0] = value

        # In multiple invocations, emit links that don't get tangled.
        self.unique_prefix = 0

    def extendMarkdown(self, md, md_globals):
        """ Add BridgePreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('bridge',
                                 BridgePreprocessor(md),
                                 ">normalize_whitespace")

class BridgePreprocessor(Preprocessor):
    BRIDGE_RE = re.compile(r'\[bridge(?P<attribs>.*?)\](?P<data>.*?)\[\/bridge\]', re.MULTILINE | re.DOTALL | re.VERBOSE)

    def __init__(self, md):
        super(BridgePreprocessor, self).__init__(md)
        self.checked_for_bridge = False
        
    def run(self, lines):
        """ Match and store Bridge Blocks in the HtmlStash. """
        print('running')
        text = "\n".join(lines)
        while 1:
            m = self.BRIDGE_RE.search(text)
            if m:
                print('Matched!')
                
                if m.group('attribs'):
                    getAttribs = True
                if m.group('data'):
                    if re.search("\n",m.group('data')):
                        tag = "h3"
                    else:
                        tag = "span"
                    dostuff = True
                else:
                    raise Exception('No data found')

                code = "<%s>bridge here</%s>" % (tag,tag)

                placeholder = self.markdown.htmlStash.store(code, safe=True)
                text = '%s\n%s\n%s'% (text[:m.start()], placeholder, text[m.end():])
            else:
                break
        return text.split("\n")

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt


def makeExtension(configs=None):
    return BridgeExtension(configs=configs)

