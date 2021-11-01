# Welcome to Native Authenticator's documentation!

This is a relatively simple authenticator for small or medium-sized [JupyterHub](https://github.com/jupyterhub/) applications. Signup and authentication are implemented as native to JupyterHub without relying on external services.

NativeAuthenticator provides the following features:

- New users can signup on the system;
- New users can be blocked from accessing the system awaiting admin authorization;
- Option of enforcing password security by disallowing common passwords or requiring a minimum password length;
- Option to block users after a set number of failed login attempts;
- Option of open signup without need for initial authorization;
- Option of asking more information about users on signup (e-mail).
- Option of requiring users to agree with given Terms of Service;
- Option of protection against scripting attacks via reCAPTCHA;
- Option for users with an org-internal e-mail address to self-approve via secure link;

# Indices and tables

```{toctree}
:caption: 'Contents:'
:maxdepth: 2

quickstart
options
troubleshooting
```
