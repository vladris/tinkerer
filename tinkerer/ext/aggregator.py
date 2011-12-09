'''
    aggregator
    ~~~~~~~~~~

    Aggregates multiple posts into single pages.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''

# generate pages
def make_aggregated_pages(app):
    env = app.builder.env

    groups = [env.blog_posts[i:i+10] for i in range(0, len(env.blog_posts), 10)]

    for i, posts in enumerate(groups):
        context = { 
            "prev": {},
            "next": {}
        }

        context["posts"] = [env.blog_metadata[post] for post in posts]
        if i == 0:
            pagename = "index"
            context["prev"] = None
        else:
            pagename = "page%d" % i
            context["prev"]["title"] = "Newer"
            context["prev"]["link"] = "index.html" if i == 1 else "page%d.html" % (i - 1)

        if i == len(groups) - 1:
            context["next"] = None
        else:
            context["next"]["title"] = "Older"
            context["next"]["link"] = "page%d.html" % (i + 1)

        yield (pagename, context, "aggregated.html")

