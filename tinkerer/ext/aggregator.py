'''
    aggregator
    ~~~~~~~~~~

    Aggregates multiple posts into single pages.

    :copyright: Copyright 2011-2016 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import copy
from tinkerer.ext.uistr import UIStr


def make_aggregated_pages(app):
    '''
    Generates aggregated pages.
    '''
    env = app.builder.env
    posts_per_page = app.config.posts_per_page
    landing_page = app.config.landing_page

    if landing_page:
        if "pages/%s" % landing_page not in env.blog_pages:
            raise Exception("Missing landing page: %s" % landing_page)

        yield (
            "index",
            {"redirect_url": "./pages/%s.html" % landing_page},
            "index.html"
        )

    # get post groups
    groups = [env.blog_posts[i:i+posts_per_page]
              for i in range(0, len(env.blog_posts), posts_per_page)]

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
            # deepcopy metadata for each post
            metadata = copy.deepcopy(env.blog_metadata[post])
            context["posts"].append(metadata)

        pagename = "page%d" % (i + 1)

        # handle navigation
        if i == 0:
            # if landing_page, keep "page1", else use "index" so we land on
            # first aggregated page
            if not landing_page:
                pagename = "index"

            # first page doesn't have prev link and its title is "Home"
            context["prev"] = None
            context["title"] = UIStr.HOME
        else:
            # following pages prev-link to previous page (titled as "Newer")
            context["prev"]["title"] = UIStr.NEWER
            context["prev"]["link"] = "page%d.html" % i

            # if no landing_page, prev link for second page is "index"
            if i == 1 and not landing_page:
                context["prev"]["link"] = "index.html"

            context["title"] = UIStr.PAGE_FMT % (i + 1)

        if i == len(groups) - 1:
            # last page doesn't have next link
            context["next"] = None
        else:
            # other pages next-link to following page (titled as "Older")
            context["next"]["title"] = UIStr.OLDER
            context["next"]["link"] = "page%d.html" % (i + 2)

        context["archive_title"] = UIStr.BLOG_ARCHIVE

        yield (pagename, context, "aggregated.html")
