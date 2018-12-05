Quickstart
==========

Native Authenticator is a plugin Authenticator for the 
`JupyterHub <https://github.com/jupyterhub/>`_. Be sure you have JupyterHub 
already running on your machine before installing this authenticator.

You must install this authenticator throught the project's repository. This is 
a temporary solution until we have the package on the `Pypi <https://pypi.org/>`_:

.. code-block:: bash

   $ git clone https://github.com/jupyterhub/nativeauthenticator.git
   $ pip install -e .


Then, you must create the configuration file for JupyterHub:

.. code-block:: bash

    $ jupyterhub --generate-config -f /etc/jupyterhub/jupyterhub_config.py


And change the default Authenticator class for our Native Authenticator class:

`c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'`


Run your JupyterHub normally, and the authenticator will be running with it.
