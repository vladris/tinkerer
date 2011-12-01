import tinkerer
import tinkerer.paths        


# TODO: Edit the lines below
project = 'My blog'                                       # Change this to the name of your blog
tagline = 'Add intelligent tagline here'                  # Change this to the tagline of your blog
copyright = '1984, Winston Smith'                         # Change this to your copyright string
website = 'http://127.0.0.1'                              # Change this to your URL (required for RSS)


# More tweaks
disqus_shortname = None                                   # Add your Disqus shortname to enable comments
html_favicon = 'tinkerer.ico'                             # Favicon
html_theme = 'metropolish'                                # Tinkerer theme (or your own)
html_theme_options = { }                                  # Theme-specific options, see docs


# Edit lines below to further customize Sphinx build
extensions = [{{ extensions }}] # Add other Sphinx extensions here
templates_path = ['_templates', tinkerer.paths.templates] # Add other template paths here
html_static_path = ['_static', tinkerer.paths.static]     # Add other static paths here
html_theme_path = [tinkerer.paths.themes]                 # Add other theme paths here
exclude_patterns = []                                     # Add file patterns to exclude from build


# Do not modify below lines as the values are required by Tinkerer to play nice with Sphinx
source_suffix = tinkerer.source_suffix
master_doc = tinkerer.master_doc
version = tinkerer.__version__
release = tinkerer.__version__
html_title = project
html_use_index = False
html_show_sourcelink = False

