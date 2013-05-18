Hide Email Addresses From Spam Bots
===================================

Tinkerer has a simple built in mechanism to hide your email address from spambots 
by generating an obfuscated email address which than gets decrypted in the browser
with the help of a little bit JavaScript.

To insert an email address just use:

.. code-block:: rst

  :email:`tinkerer-dev <tinkerer-dev@googlegroups.com>`
  
:email:`tinkerer-dev <tinkerer-dev@googlegroups.com>`

The encrypted html looks like this:

.. code-block:: html

  <noscript>(Javascript must be enabled to see this e-mail address)</noscript>
  <script type="text/javascript">document.write(
  "<n uers=\"znvygb:gvaxrere-qri\100tbbtyrtebhcf\056pbz\">gvaxrere-qri <\057n>".replace(/[a-zA-Z]/g,
  function(c){
  return String.fromCharCode(
  (c<="Z"?90:122)>=(c=c.charCodeAt(0)+13)?c:c-26);}));
  </script>

If the user has JavaScript disabled he will see this:

.. code-block:: html

  (Javascript must be enabled to see this e-mail address)

