'''
    fbcomments
    ~~~~~~~~~~

    Handler for `comments` directive using Facebook Comment Box.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from sphinx.util.compat import Directive
from docutils import nodes



'''
Facebook JS SDK loader script.
'''
FB_JSSDK = "_static/fb.js"



def create_thread(link):
    '''
    Returns code to create a new FB comment box.
    '''
    return str(
'<div id="comments">'
'   <div class="fb-comments" data-href="%s">'
'   </div>'
'</div>' % link)



def get_count(link):
    '''
    Returns code to retrieve comment count.
    '''
    return str(
'<a href="%s#comments">'    
'<fb:comments-count href="%s"></fb:comments-count> comment(s)' 
'</a>' % (link, link))



def add_fbcomments(app, pagename, templatename, context, doctree):
    '''
    Adds Facebook comments to page.
    '''
    env = app.builder.env

    # append fb.js if not already in context
    if FB_JSSDK not in context["script_files"]:
        context["script_files"].append(FB_JSSDK)

    # if page is blog post and has comments
    if pagename in env.blog_metadata and env.blog_metadata[pagename].comments:
        link = app.config.website + env.blog_metadata[pagename].link + ".html"

        context["comments"] = create_thread(link)

        # store code required to retrieve comment count for this post in metadata
        env.blog_metadata[pagename].comment_count = get_count(link)



def setup(app):
    '''
    Sets up Facebook comment handler.
    '''
    # connect event
    app.connect("html-page-context", add_fbcomments)

