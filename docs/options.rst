Feature Options
===============

Password Strength
----------------

By default, when a user signs up through Native Authenticator there is no password strength verification. There are two methods that you can add to increase password strength: a verification for commmon passowords and a minimum length of password. 

To verify if the password is not common (such as 'qwerty' or '1234'), you can add the following line to your config file:

.. code-block:: python

    c.Authenticator.check_common_password = True

The Authenticator will verify if the password is a common password and the user won't be able to sign up if it is. The list of the common passwords that are in our verification is available `on this link <https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt>`_ >._  


You can also add a minimum password length that the user must have. To do this add the following line on the config file with an integer as a value:

.. code-block:: python

    c.Authenticator.minimim_password_length = 10
