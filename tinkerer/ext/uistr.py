'''
    uistr
    ~~~~~

    Centralizes UI strings for easier localization and handling unicode
    support.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
try:
    # Python 3
    import builtins as __builtin__
except:
    # Python 2
    import __builtin__
    


# check whether unicode builtin exists, otherwise strings are unicode by 
# default so it can be stubbed
if "unicode" not in __builtin__.__dict__:
    def unicode(ret, ignore):
        return ret



class UIStr:
    # initialize localized strings
    def __init__(self, app):
        _ = app.t.gettext

        UIStr.HOME = unicode(_("Home"), "utf-8")
        UIStr.RECENT_POSTS = unicode(_("Recent Posts"), "utf-8")
        UIStr.POSTED_BY = unicode(_("Posted by"), "utf-8")
        UIStr.BLOG_ARCHIVE = unicode(_("Blog Archive"), "utf-8")
        UIStr.FILED_UNDER = unicode(_("Filed under"), "utf-8")
        UIStr.TAGS = unicode(_("Tags"), "utf-8")
        UIStr.TAGS_CLOUD = unicode(_("Tags Cloud"), "utf-8")
        UIStr.CATEGORIES = unicode(_("Categories"), "utf-8")
        UIStr.TIMESTAMP_FMT = unicode(_('%B %d, %Y'), "utf-8")
        UIStr.TAGGED_WITH_FMT = unicode(_('Posts tagged with <span class="title_tag">%s</span>'), "utf-8")
        UIStr.FILED_UNDER_FMT = unicode(_('Filed under <span class="title_category">%s</span>'), "utf-8")
        UIStr.NEWER = unicode(_("Newer"), "utf-8")
        UIStr.OLDER = unicode(_("Older"), "utf-8")
        UIStr.PAGE_FMT = unicode(_("Page %d"), "utf-8")
        UIStr.READ_MORE = unicode(_("Read more..."), "utf-8")
        UIStr.MAIL_HIDDEN_BY_JAVASCRIPT = unicode(_("Javascript must be enabled to see this e-mail address"), "utf-8")

