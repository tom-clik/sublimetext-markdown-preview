
'''
Use `///================ id.class ===============/// syntax to divide doc into sections

## Usage

Number of slashes at front determines section depth.

For little ad hoc sections use arbitrary amounts of slashes 

    ////========= .myclass ==============////


To manually close a div (usually after the above), use (at least 8:

    //////////

Dependencies
------------

* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)


Copyright
---------


All rights reserved.

This software is released under the modified BSD License. 
See LICENSE.md for details.


Further credits
---------------


'''


import re
from markdown.util import etree
from markdown import Extension
from markdown.treeprocessors import Treeprocessor


__version__ = "1.02.1"


class OutlineProcessor(Treeprocessor):
    def process_nodes(self, node):
        s = []
        
        pattern = re.compile('^(\/+)\={4,}\s*(?P<id>\w*)(?P<class>\.\w*)?\s*\={4,}(\/*)\s*$')
        
        endpattern = re.compile('^\/{8,}\W*$')
        for child in node.getchildren():
               
            openmatch = None 
            closematch = None

            if child.tag.lower() == 'p':
                openmatch = pattern.match(child.text)
                if not openmatch:
                    closematch = endpattern.match(child.text)

            if openmatch:
                
                depth = len(openmatch.group(1))

                # this isn't just a check -- use lots to just ensure next level up
                if depth > len(s) + 1:
                    depth = len(s) + 1

                sectionid = openmatch.group('id')
                sectionclass = openmatch.group('class')
                
                section = etree.SubElement(node, self.wrapper_tag)
                section.tail = "\n"

                node.remove(child)

                if sectionid:
                    section.attrib['id'] = sectionid

                if sectionclass:
                    section.attrib['class'] = sectionclass.strip('.')

                contained = False

                while s:
                    container, container_depth = s[-1]
                    if depth <= container_depth:
                        s.pop()
                    else:
                        contained = True
                        break

                if contained:
                    container.append(section)
                    node.remove(section)

                s.append((section, depth))

            elif closematch:

                s.pop()
                container, container_depth = s[-1]
                node.remove(child)

            else:

                if s:
                    container, container_depth = s[-1]
                    container.append(child)
                    node.remove(child)

    def run(self, root):
        self.wrapper_tag = self.config.get('wrapper_tag')[0]
        self.process_nodes(root)
        
        return root


class OutlineExtension(Extension):
    def __init__(self, configs):
        self.config = {
            'wrapper_tag': ['div', 'Tag name to use, default: div'],
        }
        for key, value in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        ext = OutlineProcessor(md)
        ext.config = self.config
        md.treeprocessors.add('outline', ext, '_end')


def makeExtension(configs={}):
    return OutlineExtension(configs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
