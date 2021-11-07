# Errors & Troubleshooting

These are some common problems that users sometimes run into and their respective solutions.

If you find yourself running into issues that are not resolved with the advice found here, please consider [opening an issue or filing a bug report](https://github.com/jupyterhub/nativeauthenticator/issues).

## Unable to log in with admin account

We often hear about problems with logging in with admin accounts on a fresh install. Note that adding an account into the `admin_users` configuration as shown below does not also create that account.
You still need to sign up an account of that name and set a password (see also the [relevant documentation](https://native-authenticator.readthedocs.io/en/latest/quickstart.html#adding-new-users)).
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
