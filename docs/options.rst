Feature Options
===============

Password Strength
----------------

You can add a verification for password strength on Sign Up by adding the following parameter to your config file:

.. code-block:: python

    c.Authenticator.check_password_strength = True

The authenticator will then verify if the user password contains at least one upper case letter, one lower case letter and a number. The default is false.

