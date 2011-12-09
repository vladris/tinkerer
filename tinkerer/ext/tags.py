'''
    tags
    ~~~~

    Extension handling post tagging.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
from sphinx.util.compat import Directive
import tinkerer.utils


# initialize tags
def initialize(app):
    app.builder.env.blog_tags = dict()


# tags directive
class TagsDirective(Directive):
    required_arguments = 0
    optional_arguments = 100
    has_content = False

    def run(self):
        # store tags to build tag pages
        env = self.state.document.settings.env

        for tag in " ".join(self.arguments).split(","):
            tag = tag.strip()
            if tag == "none":
                continue

            if tag not in env.blog_tags:
                env.blog_tags[tag] = []
            env.blog_tags[tag].append(env.docname)
            env.blog_metadata[env.docname].tags.append((tinkerer.utils.filename_from_title(tag), tag))

        return []


# generate tag pages
def make_tag_pages(app):
    env = app.builder.env

    # create a page for each tag
    for tag in env.blog_tags:
        pagename = "tags/" + tinkerer.utils.filename_from_title(tag)
        context = {
            "title": "Posts tagged with <span class='title_tag'>%s<span>" % tag,
        }
        context["years"] = dict()

        for post in env.blog_posts:
            if post not in env.blog_tags[tag]:
                continue

            year = env.blog_metadata[post].year
            if year not in context["years"]:
                context["years"][year] = []
            context["years"][year].append(env.blog_metadata[post])

        yield (pagename, context, "archive.html")

