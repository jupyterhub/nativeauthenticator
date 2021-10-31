# Contributing to Native Authenticator

Welcome! As a [Jupyter](https://jupyter.org) project,
you can follow the [Jupyter contributor guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

Make sure to also follow [Project Jupyter's Code of Conduct](https://github.com/jupyter/governance/blob/master/conduct/code_of_conduct.md)
for a friendly and welcoming collaborative environment.

## Setting up a development environment

### Install requirements

First install [JupyterHub](https://github.com/jupyterhub/jupyterhub). Then you can install de development requirements for Native Authenticator:

```shell
pip install -r dev-requirements.txt
```

And then installing Native Authenticator from master branch:

```shell
pip install -e .
```

### Running your local project

For developing the Native Authenticator, you can start a JupyterHub server using `dev-jupyterhub_config.py`.

```shell
jupyterhub -f dev-jupyterhub_config.py
```

### Runing tests

On the project folder you can run tests by using pytest

```shell
pytest
```
