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
import xml.dom.minidom



def patch_links(body, docpath, docname=None, link_title=False):
    '''
    Parses the document body and calls patch_node from the document root
    to fix hyperlinks. Also hyperlinks document title. Returns resulting 
    XML as string.
    '''
    doc = xml.dom.minidom.parseString(body.encode("utf-8"))

    patch_node(doc, docpath)

    if link_title:
        return hyperlink_title(doc.toxml(), docpath, docname)
    else:
        return doc.toxml()



def hyperlink_title(body, docpath, docname):
    body = body.replace("<h1>", '<a href="%s.html"><h1>' % 
            (docpath + docname), 1)
    body = body.replace("</h1>", "</h1></a>", 1)
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

