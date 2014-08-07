import markdown

# Set the test to one of the options here and run.
test = "footnotes"

if test == "tables":
    text = """|------------- | ------------- |
|Content Cell  | Content Cell  |
|Content Cell                 ||"""

    md = markdown.Markdown(['tables'])
    print (md.convert(text))

elif test == "alphameta":

    text = """@Title    A Test Doc.
    
The body. This is paragraph one.

@test second meta
@test third meta"""

    md = markdown.Markdown(['alphameta'])
    print (md.convert(text))
    print (md.Meta)


elif test == "admonition":

    text = """!!! note"
    
    1. Another line here.

    1. And another line

What happens here"""

    md = markdown.Markdown(['admonition'])
    print (md.convert(text))

elif test == "footnotes":

    text = """# Heading
    
The body. This is paragraph one[^nonsense].

This is also nonsense.

[^nonsense]: Nonsense makes no nense"""

    md = markdown.Markdown(['footnotes'])
    print (md.convert(text))