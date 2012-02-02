'''
    Tinkerer Setup
    ~~~~~~~~~~~~~~

    Package setup script.

    :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
from setuptools import setup, find_packages
import sys
import tinkerer



long_desc = '''
Tinkerer is a blogging engine/static website generator powered by Sphinx.

It allows blogging in reStructuredText format, comes with out-of-the-box 
support for post publishing dates, authors, categories, tags, post archive,
RSS feed generation, comments powered by Disqus and more.

Tinkerer is also highly customizable through Sphinx extensions.
'''


requires = ["Jinja2>=2.3", "Sphinx>=1.1", "argparse>=1.2"]



setup(
    name = "Tinkerer",
    version = tinkerer.__version__,
    url = "http://tinkerer.me/",
    download_url = "http://pypi.python.org/pypi/Tinkerer",
    license = "FreeBSD",
    author = "Vlad Riscutia",
    author_email = "riscutiavlad@gmail.com",
    description = "Sphinx-based blogging engine",
    long_description = long_desc,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Internet"
    ],
    platforms = "any",
    packages = find_packages(exclude=["tinkertest"]),
    include_package_data = True,
    entry_points = {
        "console_scripts": [
            "tinker = tinkerer.cmdline:main"
        ]
    },
    install_requires = requires
)
