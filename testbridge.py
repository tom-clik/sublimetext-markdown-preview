import markdown
import tempfile
import webbrowser
import os
import re

text = '''
Any old shit really

inline [bridge].63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85[/bridge]

[bridge]
[Vulnerable "None|All|NS|EW"]
[Deal "S:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85"]
[Scoring "IMP"]
[Declarer "S"]
[Contract "5HX"]
[Result "9"]
% Opening bidder might not be dealer! We ignore this value.
[Auction "N"]
1D 1S 3H =1= 4S
4NT =2= X Pass Pass
5C X 5H X
Pass Pass Pass
[Note "1:non-forcing 6-9 points, 6-card"]
[Note "2:two colors: clubs and diamonds"]
[/bridge]

# and more shit'''


# BRIDGE_RE = re.compile(r'\[bridge(?P<attribs>.*?)\](?P<data>.*?)\[\/bridge\]', re.MULTILINE | re.DOTALL | re.VERBOSE)

# if BRIDGE_RE.search(text):
#     print('ok')

md = markdown.Markdown(['bridge'])
outtext = md.convert(text)

dir = tempfile.gettempdir()

filename = "needRandomFile.html"
filepath = dir + '/' + filename

f = open(filepath,'w')
f.write(outtext)
f.close() # you can omit in most cases as the destructor will call if

mybrowser = webbrowser.get('windows-default')
mybrowser.open('file:///' + filepath)
