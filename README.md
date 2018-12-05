# Native Authenticator

[JupyterHub](http://github.com/jupyter/jupyterhub/) authenticator


## Installation

While this package is not on package manager, you can clone this repository and 
install it with:

`$ pip install -e .`

You can then use this as your authenticator by adding the following line to your jupyterhub_config.py:

`c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'`


## Running tests

To run the tests locally, you can install the development dependencies:

`$ pip install dev-requirements.txt`

Then run tests with pytest:

`$ pytest`

