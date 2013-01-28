Shell-Session Pygments Formatting
=================================

You have three possibilities:

- ``.. code-block:: bash``
- ``.. code-block:: console``
- ``.. code-block:: shell-session`` (new)

Have a look at :ref:`comparison`.

To have the same style as in the comparison just copy :download:`this file <../_static/pygments.css>`
into your ``_static`` folder.

You can also change the color of your command prompt inside ``pygments.css``:

.. code-block:: html

  .highlight .go { color: #808080 } /* Generic.Output */
  .highlight .gp { color: #18B218; font-weight: bold } /* Generic.Prompt */


.. _comparison:

Shell Code Comparison
---------------------

code-block:: bash
~~~~~~~~~~~~~~~~~

.. literalinclude:: example.txt
   :language: bash

code-block:: console
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: example.txt
   :language: console

code-block:: shell-session
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: example.txt
   :language: shell-session
