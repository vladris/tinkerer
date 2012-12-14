Command Line Reference
======================

Tinkerer is invoked using the ``tinker`` command with one of the following
arguments:

``--setup`` or ``-s``
    
    Sets up a new blog in the current directory. This command creates 
    the required files and directories.

``--post <POST>`` or ``-p <POST>``
    
    Creates a new post with the title ``<POST>``. The filename is 
    normalized by replacing all non-alphanumeric characters with ``_``. The
    file path is determined based on date as ``$(YEAR)/$(MONTH)/$(DAY)``. By
    default, current date is used.

    The new document is automatically inserted in the master document file so 
    it is picked up by the build.

    Alternately, if ``<POST>`` is the path to an already existing file, 
    Tinkerer will move the given file to the ``$(YEAR)/$(MONTH)/$(DAY)`` 
    directory corresponding to the current date and will insert the document 
    in the master document so it is picked up by the build. This is how drafts 
    are promoted to posts. 

``--date <yyyy/mm/dd>`` (can only be used with ``--post`` command above)

    Creates a new post (or publishes a draft) at the specified date.

``--page <PAGE>``
    
    Creates a new page with the title ``<PAGE>`` under the ``pages``
    directory. The filename is normalized and the new document is 
    automatically appended to the master document file so it is picked up 
    by the build.

    Alternately, if ``<PAGE>`` is the path to an already existing file, 
    Tinkerer will move the given file to the ``pages`` directory and will
    append the document at the end of the master document file so it is picked
    up by the build. This is how drafts are promoted to pages. 

``--draft <DRAFT>`` or ``-d <DRAFT>``

    Creates a new draft with the title ``<DRAFT>`` under the ``drafts`` 
    directory. The filename is normalized. The new document will be ignored by
    the Sphinx build until it is promoted to a post or a page (see above).

    Alternately, is ``<DRAFT>`` is the path to an already existing file,
    Tinkerer will move the given file to the ``drafts`` directory and will
    remove the document from the master document file so it will no longer get
    built. This is how posts and pages are demoted to drafts.

``--build`` or ``-b``

    Runs a clean Sphinx build. First, the ``blog/`` directory is cleaned up
    (all files are removed) then Sphinx build is invoked.

``--preview <PREVIEW>``

    Runs a clean Sphinx build including the draft specified by ``<PREVIEW>``.
    The draft can then be previewed in the browser.

``-v``

    Prints Tinkerer version information.    

.. note::

        Tinkerer does not support incremental builds because items like *Recent 
        Posts* change with each new post. Clean build is always performed.

Optional Flags
--------------

.. highlight:: bash

Verbosity can be change with one of the mutually exclusive flags:

``-q``

    Quiet - no stdout output.

``-f``

    Outputs filename only. A call to ``--setup`` will output ``conf.py``, a 
    call to ``--post`` will output the post file path, a call to ``--page``
    will output the page file path and a call to ``--build`` will output
    ``index.html``. This can be used to pipe Tinkerer, for example::

        tinker --post `Hello World!` -f | xargs vim

Back to :ref:`tinkerer_reference`.
