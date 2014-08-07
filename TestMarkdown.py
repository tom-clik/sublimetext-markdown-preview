import markdown
import tempfile
import webbrowser
import os

# Set the test to one of the options here and run.
test = "tables"

if test == "tables":
    text = """
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
2. Double dividers with no content are colspans. NB no spaces
3. Cells with three or more dashes as rows spans
4. Any cell can have its own alignment
5. Repeat separator row at bottom for footer (repeats table header)

A complex example 

    First Header  | Second Header | Third header
    ------------- | ------------- | --------------
    Row spane     | col span                     || 
    ---           | Content Cell  |: center      :

First Header  | Second Header | Third header
------------- | ------------- | --------------
Content Cell  | jhasda        | Third col
Content Cell  ||  second row
Content Cell  |sdghdf         

"""
    
    md = markdown.Markdown(['tables'])
    outtext =  md.convert(text)

elif test == "alphameta":

    text = """@Title    A Test Doc.
    
The body. This is paragraph one.

@test second meta
@test third meta"""

    md = markdown.Markdown(['alphameta'])
    outtext = md.convert(text)
    print (md.Meta)


elif test == "admonition":

    text = """!!! note"
    
    1. Another line here.

    1. And another line

What happens here"""

    md = markdown.Markdown(['admonition'])
    outtext = md.convert(text)

elif test == "footnotes":

    text = """# Heading
    
The body. This is paragraph one[^nonsense].

This is also nonsense.

[^nonsense]: Nonsense makes no nense"""

    md = markdown.Markdown(['footnotes'])
    outtext = md.convert(text)

dir = tempfile.gettempdir()

filename = "needRandomFile.html"
filepath = dir + '/' + filename

f = open(filepath,'w')
f.write(outtext)
f.close() # you can omit in most cases as the destructor will call if

mybrowser = webbrowser.get('windows-default')
mybrowser.open('file:///' + filepath)
