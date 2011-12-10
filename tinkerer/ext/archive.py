'''
    archive
    ~~~~~~~

    Archive generator.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
# generate archvie page
def make_archive(app):
    env = app.builder.env

    # create a page for each tag
    for tag in env.blog_tags:
        pagename = "archive"
        context = {
            "title": "Blog Archive"
        }
        context["years"] = dict()

        for post in env.blog_posts:
            year = env.blog_metadata[post].year
            if year not in context["years"]:
                context["years"][year] = []
            context["years"][year].append(env.blog_metadata[post])

        yield (pagename, context, "archive.html")


