# Contributing to Native Authenticator

Welcome! As a [Jupyter](https://jupyter.org) project,
you can follow the [Jupyter contributor guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

Make sure to also follow [Project Jupyter's Code of Conduct](https://github.com/jupyter/governance/blob/master/conduct/code_of_conduct.md)
for a friendly and welcoming collaborative environment.

## Setting up a development environment

### Install

```shell
pip install -e ".[test]"
```

### Configure pre-commit

[`pre-commit`](https://pre-commit.com/) is a tool we use to validate code and
autoformat it. The kind of validation and auto formatting can be inspected via
the `.pre-commit-config.yaml` file.

As the name implies, `pre-commit` can be configured to run its validation and
auto formatting just before you make a commit. By configuring it to do so, you
can avoid having to have a separate commit later that applies auto formatting.

To configure `pre-commit` to run act before you commit, you can run the
following command from the root of this repository next to the
`.pre-commit-config.yaml` file.

```shell
pip install pre-commit
pre-commit install --install-hooks
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
