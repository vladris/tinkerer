Command Line
============

Tinkerer is invoked using the ``tinker`` command with one of the following
arguments:

``--setup`` or ``-s``
    
    Sets up a new blog in the current directory. This command creates 
    the required files and directories.

``--post <POST>`` or ``-p <POST>``
    
    Creates a new post with the title ``<POST>``. The filename is 
    normalized by replacing all non-alphanumeric characters with ``_``. The
    file path is determined from the current date as 
    ``$(YEAR)/$(MONTH)/$(DATE)``. The new document is automatically 
    inserted in the master document file so it is picked up by the build.

``--page <PAGE>``
    
    Creates a new page with the title ``<PAGE>`` under the ``pages``
    directory. The filename is normalize and the new document is 
    automatically appended to the master document file so it is picked up 
    by the build.

``--build`` or ``-b``

    Runs a clean Sphinx build. First, the ``blog/`` directory is cleaned up
    (all files are removed) then Sphinx build is invoked.

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

        tinker --post `Hello World!` -f | xargs gvim

Back to :ref:`tinkerer_reference`.
