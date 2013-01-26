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
    patch_node(doc, docpath, docname)

    body = doc.toxml()
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
    marker_more = '<a name="more"> </a>'
    pos = body.find(marker_more)

    if pos == -1:
        return body

    body = body[:pos]

    # When the .. more:: directive comes after an subsection e.g.:
    #
    # Subsection
    # ----------
    #
    num_opening_divs = body.count("<div")
    num_closing_divs = body.count("</div")
    #print("num_opening_divs", num_opening_divs)
    #print("num_closing_divs", num_closing_divs)
    for i in range(num_opening_divs-num_closing_divs-1):
        body += "</div>"

    return body + ('<a class="readmore" href="%s.html#more">%s</a></div>' %
                (docpath + docname, UIStr.READ_MORE))



def patch_node(node, docpath, docname=None):
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
        # normalize image urls
        # <img alt="" src="2013/01/21/../../../_images/raspberry_pi_mod-io2_rpi-uext_light_small.jpeg"/>
        # <img alt="" src="_images/raspberry_pi_mod-io2_rpi-uext_light_small.jpeg"/>
        src.value = path.normpath(src.value).replace(":/", "://")
    # if node is hyperlink            
    elif node_name == "a":
        ref = node.getAttributeNode("href")
        # skip anchor links <a name="anchor1"></a>, <a name="more"/>
        if ref != None:
            # patch links only - either starting with "../" or having
            # "internal" class
            is_relative = ref.value.startswith("../") 
            if is_relative or "internal" in node.getAttribute("class"):
                ref.value = docpath + ref.value

            # html anchor with missing post.html
            # e.g. href="2012/08/23/#the-cross-compiler"
            # now href="2012/08/23/a_post.html#the-cross-compiler"
            ref.value = ref.value.replace("/#", "/%s.html#" % docname)

            # normalize urls so "2012/08/23/../../../_static/" becomes
            # "_static/" - we can use normpath for this, just make sure
            # to revert change on protocol prefix as normpath deduplicates
            # // (http:// becomes http:/)
            ref.value = path.normpath(ref.value).replace(":/", "://")
        # http://validator.w3.org
        # Error:  Duplicate ID id1, id2, ...
        ref_id = node.getAttributeNode("id")
        if ref_id != None:
            ref_id.value = ref_id.value + '_' + docname
    elif node_name == "div":
        # Duplicate ID overview.
        # <div class="contents local topic" id="overview">
        node_class = node.getAttributeNode("class")
        if node_class != None:
            if (node_class.value.startswith("contents") or
            node_class.value == "section"):
                node_id = node.getAttributeNode("id")
                node_id.value = node_id.value + '_' + docname
    # recurse
    for node in node.childNodes:
        patch_node(node, docpath, docname)



def strip_xml_declaration(body):
    """
    Remove XML declaration from document body.
    """
    return body.replace('<?xml version="1.0" ?>', '')

