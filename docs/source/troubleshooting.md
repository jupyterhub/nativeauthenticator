# Errors & Troubleshooting

These are some common problems that users sometimes run into and their respective solutions.

If you find yourself running into issues that are not resolved with the advice found here, please consider [opening an issue or filing a bug report](https://github.com/jupyterhub/nativeauthenticator/issues).

## Unable to log in with admin account

We often hear about problems with logging in with admin accounts on a fresh install. Note that adding an account into the `admin_users` configuration as shown below does not also create that account.
You still need to sign up an account of that name and set a password (see also the [relevant documentation](quickstart.md#adding-new-users)).
If the problem persists, make sure that your JupyterHub is using the correct configuration file.

```python
c.Authenticator.admin_users = {'my-admin-account'}
```

## Internal Server Errors (500) after upgrading to >= 1.0

One possible reason for this is that you're using an older database that doesn't have all necessary columns in the `users_info` table, as the column `login_email_sent` was only introduced in version 1.0.
You can verify this by looking into your system's journal (`journalctl`). If you find a line like the following with your error, then this is indeed the problem.

```shell
# ...
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: users_info.login_email_sent
# ...
```

To remedy this, you merely need to add the column to your `jupyterhub.sqlite` database with the command below. This is not done programatically on account of JupyterHub's SQL library [not being intended](https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table.append_column) for a use-case such as this. They therefore recommend migrating the database manually.

```shell
sqlite3 /path/to/your/jupyterhub.sqlite "ALTER TABLE users_info ADD login_email_sent Boolean NOT NULL DEFAULT (0)"
```

## Unable to log in with user account

Once a user has signed up, logging in issues can occur if the user is not allowed in JupyterHub configuration.

Either set the `allowed_users` option in the configuration file:

```py
c.Authenticator.allowed_users = {"user1", "user2", "new_user"}
```

However, setting this option in the configuration file has two drawbacks:

- admin users must also been present in this list to be able to login, even if they are present in `admin_users` list;
- this option lock the user list. Only listed users can sign up and log in. If another user needs to sign up, it must be added to `allowed_users` list and JupyterHub must be restarted with:

```sh
jupyterhub -f /etc/jupyterhub/jupyterhub_config.py
```

Another option is to set `allow_all` option in the configuration file:

```py
c.Authenticator.allow_all = True
```

These different options are detailed in [JupyterHub "Getting started" tutorial](https://jupyterhub.readthedocs.io/en/stable/tutorial/getting-started/authenticators-users-basics.html#authentication-and-user-basics).

## Usage with Docker

As users are stored in the JupyterHub database, user persistence when using Docker requires to persist JupyterHub database in a volume. For example:

```sh
docker run -p 8000:8000 -d --name jupyterhub -v path/to/data:/data quay.io/jupyterhub/jupyterhub
```

and setting in the configuration file:

```py
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"
```
