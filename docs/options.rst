Feature Options
===============

Password Strength
-----------------

By default, when a user signs up through Native Authenticator there is no password strength verification. There are two methods that you can add to increase password strength: a verification for commmon passowords and a minimum length of password. 

To verify if the password is not common (such as 'qwerty' or '1234'), you can add the following line to your config file:

.. code-block:: python

    c.Authenticator.check_common_password = True

The Authenticator will verify if the password is a common password and the user won't be able to sign up if it is. The list of the common passwords that are in our verification is available `on this link <https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt>`_ >._  


You can also add a minimum password length that the user must have. To do this add the following line on the config file with an integer as a value:

.. code-block:: python

    c.Authenticator.minimim_password_length = 10


Block users after failed logins
-------------------------------

One thing that can make systems more safe is to block users after a number of failed logins. With Native Authenticator you can add this feature by adding `allowed_failed_logins` on the config file. The default is 0, which means that the system will not block users ever.

.. code-block:: python

    c.Authenticator.allowed_failed_logins = 3

You can also define the number of seconds a user must wait before trying again. The default value is 600 seconds.

.. code-block:: python

    c.Authenticator.seconds_before_next_try = 1200


Open SignUp
-----------

By default all users that make sign up on Native Authenticator need an admin approval so 
they can actually log in the system. You can change this behavior by adding an option of 
open signup, where all users that do sign up can already log in the system. To do so, just add this line to the config file:

.. code-block:: python

    c.Authenticator.open_signup = True


Ask for extra information on SignUp
-----------------------------------

Native Authenticator is based on username and password only. But if you need extra information about the users, you can add them on the sign up. For now, you can ask for email by adding the following line:


.. code-block:: python

    c.Authenticator.ask_email_on_signup = True
