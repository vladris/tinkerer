import tinkerer
import tinkerer.paths        

project = 'Tinkerer'                   
tagline = 'Blogging for Pythonistas'                  
author = 'Vlad Riscutia'
copyright = '2011, ' + author         
website = 'http://tinkerer.me/'                              

disqus_shortname = 'tinkerer'                                   
html_favicon = 'tinkerer.ico'           
html_theme = "modern5"
rss_service = "http://feeds.feedburner.com/tinkerer"

extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus'] 
templates_path = ['_templates']
html_static_path = ['_static', tinkerer.paths.static]
html_theme_path = [tinkerer.paths.themes]                 
exclude_patterns = []                                     
html_sidebars = {
    "**": ["recent.html", 
           "get_tinkerer.html", 
           "searchbox.html", 
           "sphinx.html", 
           "get_involved.html"]
}

source_suffix = tinkerer.source_suffix
master_doc = tinkerer.master_doc
version = tinkerer.__version__
release = tinkerer.__version__
html_title = project
html_use_index = False
html_show_sourcelink = False
html_add_permalinks = None

