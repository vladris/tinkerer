'''
    patch
    ~~~~~

    Handles HTML link patching for images and cross-references. Sphinx
    generates these links as relative paths - aggregated pages and RSS
    feed require these to be patched.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import re
import xml.dom.minidom
from tinkerer.ext.uistr import UIStr

try:
    from html.entities import name2codepoint
except:
    from htmlentitydefs import name2codepoint    

try:
    import builtins as __builtin__
except:
    import __builtin__
    

# check whether unichr builtin exists, otherwise use chr
if "unichr" not in __builtin__.__dict__:
    unichr = chr
    
            

def build_html_only_codepoints():
    """
    Convert well formed HTML to XML by removing HTML only entity definitions.
    """
    html_name2codepoints = {}
    html_name2codepoints.update(name2codepoint)
    for name in ['amp', 'gt', 'lt', 'apos', 'quot']:
        if name in html_name2codepoints:
            del html_name2codepoints[name]
    return html_name2codepoints



HTML_ONLY_NAME2CODEPOINTS = build_html_only_codepoints()



def convert(s):
    """
    Take an input string s, find all things that look like SGML character 
    entities, and replace them with the Unicode equivalent.

    Source:
    http://stackoverflow.com/questions/1197981/convert-html-entities-to-ascii-in-python/1582036#1582036
    """
    matches = re.findall("&#\d+;", s)
    if len(matches) > 0:
        hits = set(matches)
        for hit in hits:
            name = hit[2:-1]
            try:
                entnum = int(name)
                s = s.replace(hit, unichr(entnum))
            except ValueError:
                pass
    matches = re.findall("&\w+;", s)
    hits = set(matches)
    amp = "&"
    if amp in hits:
        hits.remove(amp)
    for hit in hits:
        name = hit[1:-1]
        if name in HTML_ONLY_NAME2CODEPOINTS:
            s = s.replace(hit,
                          unichr(HTML_ONLY_NAME2CODEPOINTS[name]))
    s = s.replace(amp, "&")
    return s



def patch_links(body, docpath, docname=None, link_title=False):
    '''
    Parses the document body and calls patch_node from the document root
    to fix hyperlinks. Also hyperlinks document title. Returns resulting 
    XML as string.
    '''
    in_str = convert(body).encode("utf-8")
    doc = xml.dom.minidom.parseString(in_str)
    patch_node(doc, docpath)

    body = doc.toxml()
    if(docname!=None):
        body = make_read_more_link(body, docpath, docname)
    
    if link_title:
        return hyperlink_title(body, docpath, docname)
    else:
        return body



def hyperlink_title(body, docpath, docname):
    body = body.replace("<h1>", '<a href="%s.html"><h1>' % 
            (docpath + docname), 1)
    body = body.replace("</h1>", "</h1></a>", 1)
    return body



def make_read_more_link(body, docpath, docname):            
    marker_more="<!-- more -->"
    pos=body.find(marker_more)
    if(pos>-1):
      body = body[:pos]
      body = body + ('<a class="readmore" href="%s.html"><b>%s</b></a>' % 
        (docpath + docname, UIStr.READ_MORE))
    return body



def patch_node(node, docpath):
    '''
    Recursively patches links in nodes.
    '''
    node_name = node.localName

    # if node is <img>
    if node_name == "img":
        src = node.getAttributeNode("src")
        # if this is relative path (internal link)
        if src.value.startswith(".."):
            src.value = docpath + src.value 
    # if node is hyperlink            
    elif node_name == "a":
        if "internal" in node.getAttribute("class"):
            ref = node.getAttributeNode("href")
            ref.value = docpath + ref.value

    # recurse            
    for node in node.childNodes:
        patch_node(node, docpath)

