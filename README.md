# Native Authenticator


[![Circle Ci Badge](https://img.shields.io/circleci/project/github/jupyterhub/nativeauthenticator.svg)](https://circleci.com/gh/jupyterhub/nativeauthenticator)

![Code Cov](https://img.shields.io/codecov/c/github/jupyterhub/nativeauthenticator.svg)


A simple authenticator for small-medium size [JupyterHub](http://github.com/jupyter/jupyterhub/) applications.

Native Authenticator provides the following features:

* New users can signup on the system;
* New users can be blocked of accessing the system and need an admin authorization;
* Option of increase password security by avoiding common passwords or minimum password length;
* Option to block users after a number attempts of login;
* Option of open signup and no need for initial authorization;
* Option of adding more information about users on signup.


## Documentation

Documentation is available [here](https://native-authenticator.readthedocs.io)


## Running tests

To run the tests locally, you can install the development dependencies:

`$ pip install -r dev-requirements.txt`

Then run tests with pytest:

`$ pytest`

