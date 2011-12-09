'''
    twitter
    ~~~~~~~

    Twitter extension. 

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''

# add twitter_id to page context 
def add_twitter_id(app, context):
    context["twitter_id"] = app.config.twitter_id

