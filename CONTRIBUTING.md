# Contributing to Native Authenticator

Welcome! As a [Jupyter](https://jupyter.org) project,
you can follow the [Jupyter contributor guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

Make sure to also follow [Project Jupyter's Code of Conduct](https://github.com/jupyter/governance/blob/master/conduct/code_of_conduct.md)
for a friendly and welcoming collaborative environment.

## Setting up a development environment

### Install requirements

First install [JupyterHub](https://github.com/jupyterhub/jupyterhub). Then you can install de development requirements for Native Authenticator:

```
$ pip install -f dev-requirements.txt 
```

And then installing Native Authenticator from master branch:

```
$ pip install -e .
```

### Running your local project

For developing the Native Authenticator, you should create a `jupyterhub_config.py` file that has at least 3 things: a simple spawner, the NativeAuth as the default authenticator and at least one username to login as an admin. Example:


```python
# jupyter_config.py

c.JupyterHub.spawner_class = 'simplespawner.SimpleLocalProcessSpawner'
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.Authenticator.admin_users = {'admin'}
```

The SimpleLocalProcessSpawner makes it easier to develop the authenticator locally without major configurations but *it should not be used in production*.

Then you can run locally by using:

```
jupyterhub -f ~/jupyterhub_config.py
```

### Runing tests

On the project folder you can run tests by using pytest

```
$ pytest
```



