import markdown
import tempfile
import webbrowser
import os

# Set the test to one of the options here and run.
test = "bargello"

if test == "tables":
    text = """
First Header  | Second Header | Third header
------------- | ------------- | --------------
Content Cell  | jhasda       :| Third col
Content Cell  ||  ----
Content Cell  |:sdghdf   :
{: #table1 .intro title="My table" caption="This is my table caption"}

![A charming young lady](http://chivethebrigade.files.wordpress.com/2012/08/girls-920-23.jpg){: .figleft .popup width="200"}
"""
    
    md = markdown.Markdown(['tables','attr_list'])
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

    text = """!!! warning "Or custom title"
    
    1. Another line here.

    1. And another line

What happens here"""

    md = markdown.Markdown(['admonition'])
    outtext = md.convert(text)

elif test == "styles":

    text = """::imageboxleft::
    ![Alt text](http://images.com/image.jpg)
    
    Image caption
"""

    md = markdown.Markdown(['styles'])
    outtext = md.convert(text)

elif test == "footnotes":

    text = """# Heading
    
The body. This is paragraph one[^nonsense].

This is also nonsense.

[^nonsense]: Nonsense makes no nense"""

    md = markdown.Markdown(['footnotes'])
    outtext = md.convert(text)

elif test == "attr_list":

    text = """# Heading {: #myid .myclass}
    
The body. This is paragraph one.
{: #para1 .intro}

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.  
{: style="font-style:italic;"}

[My link](#myid)

"""

    md = markdown.Markdown(['attr_list'])
    outtext = md.convert(text)

elif test == "quick_table":

    text = """# Heading 
   
-Opener's double        Shortness in suit doubled
-Opener's new suits     natural or a control
-3NT                    Balanced Maximum (Ace or King in their suit)
-Opener's Pass          Nothing special--flat hand, could be 5x3x2 awful after which, responder's X=penalty
-Opener's jump to 4M    dead minimum, but 6x3x2

"""

    md = markdown.Markdown(['quick_table'])
    outtext = md.convert(text)

elif test == "mkdcomments":

    text = """# Heading 
   
<!--- these should go --->

"""

    md = markdown.Markdown(['mkdcomments'])
    outtext = md.convert(text)

elif test == "div_outlines":

    text = """/========== frontmatter.nonsense ===========/
   
//========== coverpage ===========//

# Heading 

Some more text

//========== indexpage ===========//

# Heading

more text

"""

    md = markdown.Markdown(['attr_list','div_outlines'])
    outtext = md.convert(text)

elif test == "bargello":
    g = open('c:\\git\\dm\\ClikWriter\\gfanshawe\\gfanshawe_complete.md','r',encoding='utf-8') #
    text = g.read()
    g.close()
    md = markdown.Markdown(['meta','attr_list','div_outlines',"includes",'toc']) 
    md.Meta = {'base_url':'c:\\git\\dm\\ClikWriter\\gfanshawe\\'}
    outtext = md.convert(text)
    
dir = tempfile.gettempdir()

filename = "needRandomFile.html"
filepath = dir + '/' + filename

f = open(filepath,'w')
f.write(outtext)
f.close() # you can omit in most cases as the destructor will call if

mybrowser = webbrowser.get('windows-default')
mybrowser.open('file:///' + filepath)
