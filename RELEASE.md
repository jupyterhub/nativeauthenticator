# How to make a release

`jupyterhub-nativeauthenticator` is a package [available on
PyPI](https://pypi.org/project/jupyterhub-nativeauthenticator/). These are
instructions on how to make a release on PyPI. The PyPI release is done
automatically by CI when a tag is pushed.

For you to follow along according to these instructions, you need:

- To have push rights to the [jupyterhub GitHub repository](https://github.com/jupyterhub/nativeauthenticator).
- To have [`tbump`](https://pypi.org/project/tbump) installed.

## Steps to make a release

1. Make sure `CHANGELOG.md` is up-to-date using [github-activity][] ahead of
   time in a dedicated PR.

1. Checkout main and make sure it is up to date.

   ```shell
   ORIGIN=${ORIGIN:-origin} # set to the canonical remote, e.g. 'upstream' if 'origin' is not the official repo
   git checkout main
   git fetch $ORIGIN main
   git reset --hard $ORIGIN/main
   ```

1. Update the version with `tbump`. You can see what will happen without making
   any changes with `tbump --dry-run ${VERSION}`.

   ```shell
   tbump ${VERSION}
   ```

   This will tag and publish a release, which will be finished on CI.

1. Reset the version back to dev, e.g. `2.1.0.dev` after releasing `2.0.0`

   ```shell
   tbump --no-tag ${NEXT_VERSION}.dev
   ```

[github-activity]: https://github.com/executablebooks/github-activity
