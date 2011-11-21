'''
    blog_conf
    ~~~~~~~~~

    Add additional configuration to the builder, bypassing conf.py

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import os


# additional configuration
def add_setup(app):
    if not hasattr(app.config, "html_theme_path"):
        app.config.html_theme_path = []
    app.config.html_theme_path.append(os.path.abspath("../themes"))


# setup
def setup(app):
    app.connect("builder-inited", add_setup)
