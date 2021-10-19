# Native Authenticator

[![Latest PyPI version](https://img.shields.io/pypi/v/jupyterhub-nativeauthenticator?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/jupyterhub-nativeauthenticator)
[![Documentation build status](https://img.shields.io/readthedocs/native-authenticator?logo=read-the-docs&logoColor=white)](https://native-authenticator.readthedocs.org/en/latest/)
[![GitHub Workflow Status - Test](https://img.shields.io/github/workflow/status/jupyterhub/nativeauthenticator/Test?logo=github&label=tests)](https://github.com/jupyterhub/nativeauthenticator/actions)
[![Code coverage](https://img.shields.io/codecov/c/github/jupyterhub/nativeauthenticator.svg)](https://codecov.io/github/jupyterhub/nativeauthenticator)
<br>
[![GitHub](https://img.shields.io/badge/issue_tracking-github-blue?logo=github)](https://github.com/jupyterhub/nativeauthenticator/issues)
[![Discourse](https://img.shields.io/badge/help_forum-discourse-blue?logo=discourse)](https://discourse.jupyter.org/c/jupyterhub)
[![Gitter](https://img.shields.io/badge/social_chat-gitter-blue?logo=gitter)](https://gitter.im/jupyterhub/jupyterhub)
[![Contribute](https://img.shields.io/badge/I_want_to_contribute!-grey?logo=jupyter)](https://github.com/jupyterhub/nativeauthenticator/blob/master/CONTRIBUTING.md)

This is a relatively simple authenticator for small or medium-sized [JupyterHub](http://github.com/jupyter/jupyterhub/) applications. Signup and authentication are implemented as native to JupyterHub without relying on external services.

NativeAuthenticator provides the following features:

* New users can signup on the system;
* New users can be blocked from accessing the system awaiting admin authorization;
* Option of enforcing password security by disallowing common passwords or requiring a minimum password length;
* Option to block users after a set number of failed login attempts;
* Option of open signup without need for initial authorization;
* Option of asking more information about users on signup (e-mail).
* Option of requiring users to agree with given Terms of Service;
* Option of protection against scripting attacks via reCAPTCHA;
* Option for users with an org-internal e-mail address to self-approve via secure link;

## Documentation

The latest documentation is always on readTheDocs, available [here](https://native-authenticator.readthedocs.io).

## Running tests

To run the tests locally, you can install the development dependencies like so:

`$ pip install -r dev-requirements.txt`

Then run tests with pytest:

`$ pytest`

