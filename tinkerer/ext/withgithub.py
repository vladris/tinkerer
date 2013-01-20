'''
    withgithub
    ~~~~~~~~~~

    An extension which provides support for Github Pages.
    By default Github Pages prohibit names starting with '_', but Sphinx
    requires them. To change this behavior, you need to add '.nojekyll' 
    file in a base directory. This extension automates the process.

    :copyright: Copyright 2011-2013 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import os



def sphinx_extension(app, exception):
    '''
    Wrapped up as a Sphinx Extension
    '''
    jekyll_file = os.path.join(app.outdir, '.nojekyll')
    open(jekyll_file, 'w').close()
    print("wrote '%s' file to prevent github blocking _* directories" % jekyll_file)



def setup(app):
    '''
    Setup function for Sphinx Extension
    '''
    app.add_config_value("github.nojekyll", True, '')
    app.connect("build-finished", sphinx_extension)

