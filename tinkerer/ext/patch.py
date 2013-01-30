'''
    patch
    ~~~~~

    Handles HTML link patching for images and cross-references. Sphinx
    generates these links as relative paths - aggregated pages and RSS
    feed require these to be patched.

    :copyright: Copyright 2011-2013 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from os import path
import re
import xml.etree.ElementTree as ET
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



def patch_links(app, body, docpath, docname=None, link_title=False):
    '''
    Parses the document body and calls patch_node from the document root
    to fix hyperlinks. Also hyperlinks document title. Returns resulting 
    XML as string.
    '''
    in_str = convert(body).encode("utf-8")
    doc = ET.fromstring(in_str)
    patch_node(app, doc, docpath, docname)

    #body = ET.tostring(doc, encoding="utf-8", method="xml") # Python 3.x
    body = convert(ET.tostring(doc))
    if docname:
        body = make_read_more_link(body, docpath, docname)

    if link_title:
        return hyperlink_title(body, docpath, docname)
    else:
        return body



def hyperlink_title(body, docpath, docname):
    """
    Hyperlink titles by embedding appropriate a tag inside
    h1 tags (which should only be post titles). 
    """
    body = body.replace("<h1>", '<h1><a href="%s.html">' % 
            (docpath + docname), 1)
    body = body.replace("</h1>", "</a></h1>", 1)
    return body



def make_read_more_link(body, docpath, docname):
    """
    Create "read more" link if marker exists.
    """
    marker_more = '<div id="more"> </div>'
    pos = body.find(marker_more)

    if pos == -1:
        return body

    body = body[:pos]

    # when the .. more:: directive comes after a subsection:
    body += "</div>" * (body.count("<div") - body.count("</div") - 1)

    return body + ('<a class="readmore" href="%s.html#more">%s</a></div>' %
                (docpath + docname, UIStr.READ_MORE))



def patch_node(app, node, docpath, docname=None):
    '''
    Recursively patches links in nodes.
    '''
    node_name = node.tag

    # if node is <img>
    if node_name == "img":
        src = node.get("src")
        # if this is relative path (internal link)
        if src.startswith(".."):
            src = docpath + src
        src = path.normpath(src).replace(":/", "://")
        node.set('src', src)
    # if node is hyperlink
    elif node_name == "a":
        ref = node.get("href")
        # patch links only - either starting with "../" or having
        # "internal" class
        is_relative = ref.startswith("../")
        node_class = node.get("class")
        is_internal = node_class != None and "internal" in node_class
        if is_relative or is_internal:
            ref = docpath + ref

        # html anchor with missing post.html
        # e.g. href="2012/08/23/#the-cross-compiler"
        # now href="2012/08/23/a_post.html#the-cross-compiler"
        ref = ref.replace("/#", "/%s.html#" % docname)

        # normalize urls so "2012/08/23/../../../_static/" becomes
        # "_static/" - we can use normpath for this, just make sure
        # to revert change on protocol prefix as normpath deduplicates
        # // (http:// becomes http:/)
        ref = path.normpath(ref).replace(":/", "://")
        node.set('href', ref)

    app.emit('patch-node', node, docpath, docname)

    # recurse            
    for child_node in node:
        patch_node(app, child_node, docpath, docname)



def strip_xml_declaration(body):
    """
    Remove XML declaration from document body.
    """
    return body.replace('<?xml version="1.0" ?>', '')

