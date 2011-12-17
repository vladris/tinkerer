'''
    patch
    ~~~~~

    Handles HTML link patching for images and cross-references. Sphinx
    generates these links as relative paths - aggregated pages and RSS
    feed require these to be patched.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
import xml.dom.minidom



def patch_links(body, docpath):
    '''
    Parses the document body and calls patch_node for the document root. 
    Returns resulting XML as string.
    '''
    doc = xml.dom.minidom.parseString(body)
    patch_node(doc, docpath)
    return doc.toxml()



def patch_node(node, docpath):
    '''
    Recursively patches links in nodes.
    '''
    node_name = node._get_localName()

    # if node is <img>
    if node_name == "img":
        src = node.attributes["src"]
        # if this is relative path (internal link)
        if src.value.startswith(".."):
            src.value = docpath + src.value 
    # if node is hyperlink            
    elif node_name == "a":
        # if internal hyperlink
        if "internal" in node.attributes["class"].value:
            ref = node.attributes["href"]
            ref.value = docpath + ref.value

    # recurse            
    for node in node.childNodes:
        patch_node(node, docpath)

