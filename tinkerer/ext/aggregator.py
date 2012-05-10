'''
    aggregator
    ~~~~~~~~~~

    Aggregates multiple posts into single pages.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import copy
from tinkerer.ext import patch
from tinkerer.ext.uistr import UIStr



def make_aggregated_pages(app):
    '''
    Generates aggregated pages.
    '''
    env = app.builder.env
    posts_per_page = app.config.posts_per_page

    # get post groups
    groups = [env.blog_posts[i:i+posts_per_page] for i in range(0, 
                    len(env.blog_posts), posts_per_page)]

    # for each group
    for i, posts in enumerate(groups):
        # initialize context
        context = { 
            "prev": {},
            "next": {},
            "posts": []
        }

        # add posts to context
        for post in posts:
            # deepcopy metadata and patch links
            metadata = copy.deepcopy(env.blog_metadata[post])
            metadata.body = patch.patch_links(
                    metadata.body, 
                    post[:11], # first 11 characters is path (YYYY/MM/DD/)
                    post[11:], # following characters represent filename
                    True)      # hyperlink title to post
            metadata.body = patch.strip_xml_declaration(metadata.body)
            context["posts"].append(metadata)


        # handle navigation
        if i == 0:
            # first page doesn't have prev link and its title is "Home"
            pagename = "index"
            context["prev"] = None
            context["title"] = UIStr.HOME
        else:
            # following pages prev-link to previous page (titled as "Newer")
            pagename = "page%d" % i
            context["prev"]["title"] = UIStr.NEWER
            context["prev"]["link"] = "index.html" if i == 1 else "page%d.html" % (i - 1)
            context["title"] = UIStr.PAGE_FMT % (i + 1)

        if i == len(groups) - 1:
            # last page doesn't have next link
            context["next"] = None
        else:
            # other pages next-link to following page (titled as "Older")
            context["next"]["title"] = UIStr.OLDER
            context["next"]["link"] = "page%d.html" % (i + 1)

        yield (pagename, context, "aggregated.html")

