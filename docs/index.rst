.. Native Authenticator documentation master file, created by
   sphinx-quickstart on Wed Dec  5 10:28:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Native Authenticator's documentation!
================================================

Welcome to Native Authenticator's documentation! 

Native Authenticator is a plugin Authenticator for the `JupyterHub <https://github.com/jupyterhub/>`_. Be sure you have JupyterHub already running on your machine before installing this authenticator.

Indices and tables
==================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   quickstart
   options


Installation
------------

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


User creation
-------------

To access the system you must go to `/hub/signup` and create a username and a password. Be default, all users that sings up to the system need an Admin authorization to access the system. 

If you are and admin, be sure that your username is listed on the `admin_users` on the config file such as:

.. code-block:: python

    c.Authenticator.admin_users = {'username'}

If you create a new user that is listed as an admin on the config file, it will automatically have access to the system just after the signup. 


Authorize new users
-------------------

To authorize new users to enter the system or to manage those that already have access to the system you can go to `<ip:port>/hub/authorize`. 

