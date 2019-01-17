Feature Options
===============

Password Strength
----------------

By default, when a user signs up through Native Authenticator there is no password strength verification. If you need this, you can add a verification for password strength by adding the following parameter to your config file:

.. code-block:: python

    c.Authenticator.check_password_strength = True

The Authenticator will verify if the password has at least 8 characters and if it not a common password. The list of the common passwords it checks is available `on this link <https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt>`_ >._  


By default the Authenticator will verify if the password is at least 8 characters long. If you, however, need something different, you can change the minimum size adding this parameter to the config file:

.. code-block:: python

    c.Authenticator.password_length = 10
