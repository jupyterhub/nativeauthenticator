# Changelog

<!--
The changelog should be updated using the tool `github-activity --heading-level=3`.

To install and configure it, see https://github.com/executablebooks/github-activity#readme.
-->

## 1.3

### 1.3.0 - 2024-09-17

With this release, `jupyterhub` 4.1.6 and Python 3.9 or higher becomes required.

([full changelog](https://github.com/jupyterhub/nativeauthenticator/compare/1.2.0...1.3.0))

#### Bugs fixed

- Fix user was added on sign-up even if password didn't match confirmation [#275](https://github.com/jupyterhub/nativeauthenticator/pull/275) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Fix page.html menu bar [#270](https://github.com/jupyterhub/nativeauthenticator/pull/270) ([@paolocarinci](https://github.com/paolocarinci), [@manics](https://github.com/manics), [@lambdaTotoro](https://github.com/lambdaTotoro))

#### Maintenance and upkeep improvements

- Update .flake8 config to match other jupyterhub repos [#276](https://github.com/jupyterhub/nativeauthenticator/pull/276) ([@consideRatio](https://github.com/consideRatio))
- Require jupyterhub 4.1.6+ and Python 3.9+ [#274](https://github.com/jupyterhub/nativeauthenticator/pull/274) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Update rtd build environment etc [#273](https://github.com/jupyterhub/nativeauthenticator/pull/273) ([@consideRatio](https://github.com/consideRatio))

#### Continuous integration improvements

- build(deps): bump codecov/codecov-action from 3 to 4 [#263](https://github.com/jupyterhub/nativeauthenticator/pull/263) ([@consideRatio](https://github.com/consideRatio))
- build(deps): bump actions/setup-python from 4 to 5 [#260](https://github.com/jupyterhub/nativeauthenticator/pull/260) ([@consideRatio](https://github.com/consideRatio))
- build(deps): bump actions/checkout from 3 to 4 [#254](https://github.com/jupyterhub/nativeauthenticator/pull/254) ([@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/nativeauthenticator/graphs/contributors?from=2023-05-22&to=2024-09-17&type=c))

@consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AconsideRatio+updated%3A2023-05-22..2024-09-17&type=Issues)) | @lambdaTotoro ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AlambdaTotoro+updated%3A2023-05-22..2024-09-17&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Amanics+updated%3A2023-05-22..2024-09-17&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aminrk+updated%3A2023-05-22..2024-09-17&type=Issues)) | @paolocarinci ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Apaolocarinci+updated%3A2023-05-22..2024-09-17&type=Issues))

## 1.2

### 1.2.0 - 2023-05-22

The release adds support for JupyterHub 4.

([full changelog](https://github.com/jupyterhub/nativeauthenticator/compare/1.1.0...1.2.0))

#### Enhancements made

- Register native as an jupyterhub authenticator class [#247](https://github.com/jupyterhub/nativeauthenticator/pull/247) ([@consideRatio](https://github.com/consideRatio))

#### Maintenance and upkeep improvements

- Add test as optional dependency, refactor fixtures to conftest.py, fix code coverage setup [#245](https://github.com/jupyterhub/nativeauthenticator/pull/245) ([@consideRatio](https://github.com/consideRatio))
- pre-commit: add autoflake, use isort over reorder-python-imports [#244](https://github.com/jupyterhub/nativeauthenticator/pull/244) ([@consideRatio](https://github.com/consideRatio))
- maint: transition to pypi trusted workflow release, put tbump conf in pyproject.toml [#243](https://github.com/jupyterhub/nativeauthenticator/pull/243) ([@consideRatio](https://github.com/consideRatio))
- Add xsrf token to the login, signup, and password changing pages [#239](https://github.com/jupyterhub/nativeauthenticator/pull/239) ([@agostof](https://github.com/agostof))
- Use XSRF tokens for cross-site protections [#236](https://github.com/jupyterhub/nativeauthenticator/pull/236) ([@djangoliv](https://github.com/djangoliv))
- dependabot: rename to .yaml [#235](https://github.com/jupyterhub/nativeauthenticator/pull/235) ([@consideRatio](https://github.com/consideRatio))
- dependabot: monthly updates of github actions [#233](https://github.com/jupyterhub/nativeauthenticator/pull/233) ([@consideRatio](https://github.com/consideRatio))

#### Continuous integration improvements

- ci: pin sqlalchemy 1 on jupyterhub 1 and 2 [#240](https://github.com/jupyterhub/nativeauthenticator/pull/240) ([@minrk](https://github.com/minrk))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/nativeauthenticator/graphs/contributors?from=2022-09-09&to=2023-05-21&type=c))

[@agostof](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aagostof+updated%3A2022-09-09..2023-05-21&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AconsideRatio+updated%3A2022-09-09..2023-05-21&type=Issues) | [@djangoliv](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Adjangoliv+updated%3A2022-09-09..2023-05-21&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aminrk+updated%3A2022-09-09..2023-05-21&type=Issues)

## 1.1

### 1.1.0 - 2022-09-09

([full changelog](https://github.com/jupyterhub/nativeauthenticator/compare/1.0.5...1.1.0))

#### Enhancements made

- Ask for new passwords twice, ask for current password on change [#180](https://github.com/jupyterhub/nativeauthenticator/pull/180) ([@lambdaTotoro](https://github.com/lambdaTotoro))

#### Bugs fixed

- Add slash restriction to username validation [#197](https://github.com/jupyterhub/nativeauthenticator/pull/197) ([@marc-marcos](https://github.com/marc-marcos))
- Correct login procedure for admins [#195](https://github.com/jupyterhub/nativeauthenticator/pull/195) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- Enforce password criteria on password change [#169](https://github.com/jupyterhub/nativeauthenticator/pull/169) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- Systematic refresh of templates [#162](https://github.com/jupyterhub/nativeauthenticator/pull/162) ([@consideRatio](https://github.com/consideRatio))

#### Maintenance and upkeep improvements

- document and refactor the handlers [#183](https://github.com/jupyterhub/nativeauthenticator/pull/183) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- chore: use async instead of gen.coroutine [#178](https://github.com/jupyterhub/nativeauthenticator/pull/178) ([@consideRatio](https://github.com/consideRatio))
- pre-commit: apply black formatting [#174](https://github.com/jupyterhub/nativeauthenticator/pull/174) ([@consideRatio](https://github.com/consideRatio))
- Smaller tweaks from pre-commit autoformatting hooks [#173](https://github.com/jupyterhub/nativeauthenticator/pull/173) ([@consideRatio](https://github.com/consideRatio))
- Support JupyterHub 2's fine grained RBAC permissions, and test against Py3.10 and JH2 [#160](https://github.com/jupyterhub/nativeauthenticator/pull/160) ([@consideRatio](https://github.com/consideRatio))

#### Documentation improvements

- update documentation screenshots [#194](https://github.com/jupyterhub/nativeauthenticator/pull/194) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- docs: fix c.JupyterHub.template_paths [#192](https://github.com/jupyterhub/nativeauthenticator/pull/192) ([@yapatta](https://github.com/yapatta))
- docs: c.NativeAuthenticator instead of c.Authenticator [#188](https://github.com/jupyterhub/nativeauthenticator/pull/188) ([@consideRatio](https://github.com/consideRatio))
- docs: update from rST to MyST and to common theme [#187](https://github.com/jupyterhub/nativeauthenticator/pull/187) ([@consideRatio](https://github.com/consideRatio))
- document and refactor the handlers [#183](https://github.com/jupyterhub/nativeauthenticator/pull/183) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- docs: add inline documentation to orm.py [#179](https://github.com/jupyterhub/nativeauthenticator/pull/179) ([@consideRatio](https://github.com/consideRatio))
- Update CONTRIBUTING.md [#161](https://github.com/jupyterhub/nativeauthenticator/pull/161) ([@consideRatio](https://github.com/consideRatio))

#### Continuous integration improvements

- ci: add RELEASE.md and tbump.toml [#217](https://github.com/jupyterhub/nativeauthenticator/pull/217) ([@consideRatio](https://github.com/consideRatio))
- ci: add tests against jupyterhub 3 and python 3.11 [#216](https://github.com/jupyterhub/nativeauthenticator/pull/216) ([@consideRatio](https://github.com/consideRatio))
- ci: add dependabot bumping of github actions [#215](https://github.com/jupyterhub/nativeauthenticator/pull/215) ([@consideRatio](https://github.com/consideRatio))
- ci: rely on pre-commit.ci & run tests only if needed [#175](https://github.com/jupyterhub/nativeauthenticator/pull/175) ([@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/nativeauthenticator/graphs/contributors?from=2021-10-19&to=2022-09-09&type=c))

[@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AconsideRatio+updated%3A2021-10-19..2022-09-09&type=Issues) | [@harshu1470](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aharshu1470+updated%3A2021-10-19..2022-09-09&type=Issues) | [@lambdaTotoro](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AlambdaTotoro+updated%3A2021-10-19..2022-09-09&type=Issues) | [@leportella](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aleportella+updated%3A2021-10-19..2022-09-09&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Amanics+updated%3A2021-10-19..2022-09-09&type=Issues) | [@marc-marcos](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Amarc-marcos+updated%3A2021-10-19..2022-09-09&type=Issues) | [@yapatta](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Ayapatta+updated%3A2021-10-19..2022-09-09&type=Issues)

## 1.0

### 1.0.5 - 2021-10-19

This releases resolves an incorrect Python module structure that lead to a failing import when installing from a built wheel.

([full changelog](https://github.com/jupyterhub/nativeauthenticator/compare/1.0.4...1.0.5))

### 1.0.4 - 2021-10-19

This release includes a bugfix related to an import statement.

([full changelog](https://github.com/jupyterhub/nativeauthenticator/compare/1.0.3...1.0.4))

### 1.0.3 - 2021-10-19

This release includes a bugfix of an import statement.

([full changelog](https://github.com/jupyterhub/nativeauthenticator/compare/1.0.2...1.0.3))

### 1.0.2 - 2021-10-19

This release includes documentation updates and an attempted bugfix of an import statement.

([full changelog](https://github.com/jupyterhub/nativeauthenticator/compare/1.0.1...1.0.2))

### 1.0.1 - 2021-10-18

A small release hiccup resolved.

([full changelog](https://github.com/jupyterhub/nativeauthenticator/compare/1.0.0...1.0.1))

### 1.0.0 - 2021-10-18

As tracked by #149 and especially since the incorporation of multiple substantial and new features, we are now happy to call this version 1.0.0.

#### What's Changed

Here are the main contributions in this release:

- Unauthorized users now get a better error message on failed login (#119)
- GitHub Page About Section now links to Docs (#143)
- Improved documentation
- feat: keep position in authorization area by @djangoliv in https://github.com/jupyterhub/nativeauthenticator/pull/141
- Feature/page template by @raethlein in https://github.com/jupyterhub/nativeauthenticator/pull/79

A very warm and special thanks goes out to @consideRatio who helped tremendously in keeping the project up to date:

- Update changelog from 0.0.1-0.0.7: https://github.com/jupyterhub/nativeauthenticator/pull/137
- Add various README badges: https://github.com/jupyterhub/nativeauthenticator/pull/135
- ci: transition from circleci to github workflows: https://github.com/jupyterhub/nativeauthenticator/pull/134
- ci: add publish to pypi workflow: https://github.com/jupyterhub/nativeauthenticator/pull/136

Special shoutout also goes to @davidedelvento who contributed a lot of work in these PRs:

- Terms of Service: https://github.com/jupyterhub/nativeauthenticator/pull/148
- Recaptcha: https://github.com/jupyterhub/nativeauthenticator/pull/146
- Allow some users (but not all) to not need admin approval: https://github.com/jupyterhub/nativeauthenticator/pull/145

**Full Changelog**: https://github.com/jupyterhub/nativeauthenticator/compare/0.0.7...1.0.0

## 0.0

### 0.0.7 - 2021-01-14

#### Merged PRs

- fix: we now need to await render_template method [#129](https://github.com/jupyterhub/nativeauthenticator/pull/129) ([@djangoliv](https://github.com/djangoliv))
- Bump notebook from 5.7.8 to 6.1.5 [#125](https://github.com/jupyterhub/nativeauthenticator/pull/125) ([@dependabot](https://github.com/dependabot))

#### Contributors to this release

[@dependabot](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Adependabot+updated%3A2020-11-12..2021-01-11&type=Issues) | [@djangoliv](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Adjangoliv+updated%3A2020-11-12..2021-01-11&type=Issues) | [@lambdaTotoro](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AlambdaTotoro+updated%3A2020-11-12..2021-01-11&type=Issues)

### 0.0.6 - 2020-11-14

#### Merged PRs

- Discard from authorize [#121](https://github.com/jupyterhub/nativeauthenticator/pull/121) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- Allowed users [#120](https://github.com/jupyterhub/nativeauthenticator/pull/120) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- Ensure that jinja loader is not registered at each render [#115](https://github.com/jupyterhub/nativeauthenticator/pull/115) ([@fbessou](https://github.com/fbessou))
- Allow admin to change any password [#112](https://github.com/jupyterhub/nativeauthenticator/pull/112) ([@djangoliv](https://github.com/djangoliv))
- Bump notebook from 5.7.2 to 5.7.8 [#111](https://github.com/jupyterhub/nativeauthenticator/pull/111) ([@dependabot](https://github.com/dependabot))
- Signup error [#109](https://github.com/jupyterhub/nativeauthenticator/pull/109) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- fix broken test [#107](https://github.com/jupyterhub/nativeauthenticator/pull/107) ([@leportella](https://github.com/leportella))
- fix flake8 errors [#106](https://github.com/jupyterhub/nativeauthenticator/pull/106) ([@leportella](https://github.com/leportella))
- Add option for disable user to signup [#103](https://github.com/jupyterhub/nativeauthenticator/pull/103) ([@mayswind](https://github.com/mayswind))
- Error on signup with taken username [#102](https://github.com/jupyterhub/nativeauthenticator/pull/102) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- add changelog [#101](https://github.com/jupyterhub/nativeauthenticator/pull/101) ([@leportella](https://github.com/leportella))
- fix orm for support mysql [#57](https://github.com/jupyterhub/nativeauthenticator/pull/57) ([@00Kai0](https://github.com/00Kai0))

#### Contributors to this release

[@00Kai0](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3A00Kai0+updated%3A2020-02-20..2020-11-12&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Adependabot+updated%3A2020-02-20..2020-11-12&type=Issues) | [@djangoliv](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Adjangoliv+updated%3A2020-02-20..2020-11-12&type=Issues) | [@fbessou](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Afbessou+updated%3A2020-02-20..2020-11-12&type=Issues) | [@lambdaTotoro](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AlambdaTotoro+updated%3A2020-02-20..2020-11-12&type=Issues) | [@leportella](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aleportella+updated%3A2020-02-20..2020-11-12&type=Issues) | [@mayswind](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Amayswind+updated%3A2020-02-20..2020-11-12&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aminrk+updated%3A2020-02-20..2020-11-12&type=Issues) | [@shreeishitagupta](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Ashreeishitagupta+updated%3A2020-02-20..2020-11-12&type=Issues)

### 0.0.5 - 2020-02-20

#### Merged PRs

- Revert "fix timedelta.seconds misuse" [#100](https://github.com/jupyterhub/nativeauthenticator/pull/100) ([@leportella](https://github.com/leportella))
- upgrade version to launch at pypi [#99](https://github.com/jupyterhub/nativeauthenticator/pull/99) ([@leportella](https://github.com/leportella))
- Add announcement_login handling to login template [#97](https://github.com/jupyterhub/nativeauthenticator/pull/97) ([@JohnPaton](https://github.com/JohnPaton))
- add contributing file [#89](https://github.com/jupyterhub/nativeauthenticator/pull/89) ([@leportella](https://github.com/leportella))
- Add normalization to username [#87](https://github.com/jupyterhub/nativeauthenticator/pull/87) ([@leportella](https://github.com/leportella))
- Authenticator should accept passwords that are exactly the minimum length [#86](https://github.com/jupyterhub/nativeauthenticator/pull/86) ([@lambdaTotoro](https://github.com/lambdaTotoro))
- Add missing base_url prefix to links for correct routing [#83](https://github.com/jupyterhub/nativeauthenticator/pull/83) ([@raethlein](https://github.com/raethlein))
- fix timedelta.seconds misuse [#82](https://github.com/jupyterhub/nativeauthenticator/pull/82) ([@meownoid](https://github.com/meownoid))
- fix typos and improve performance [#81](https://github.com/jupyterhub/nativeauthenticator/pull/81) ([@meownoid](https://github.com/meownoid))
- Add check for None before trying to delete a user. [#80](https://github.com/jupyterhub/nativeauthenticator/pull/80) ([@raethlein](https://github.com/raethlein))
- Fix failed to change password due to compatibility issues with JupyterHub 1.0.0 [#78](https://github.com/jupyterhub/nativeauthenticator/pull/78) ([@hiroki-sawano](https://github.com/hiroki-sawano))
- postgres says `opt_secret` is too long for `varying(10)` [#76](https://github.com/jupyterhub/nativeauthenticator/pull/76) ([@databasedav](https://github.com/databasedav))
- Add 2 factor authentication as optional feature [#70](https://github.com/jupyterhub/nativeauthenticator/pull/70) ([@leportella](https://github.com/leportella))
- Add stylized login page [#69](https://github.com/jupyterhub/nativeauthenticator/pull/69) ([@leportella](https://github.com/leportella))
- Add importation of db from FirstUse Auth [#67](https://github.com/jupyterhub/nativeauthenticator/pull/67) ([@leportella](https://github.com/leportella))
- Change setup to version 0.0.4 [#65](https://github.com/jupyterhub/nativeauthenticator/pull/65) ([@leportella](https://github.com/leportella))

#### Contributors to this release

[@chicocvenancio](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Achicocvenancio+updated%3A2019-02-15..2020-02-20&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Acholdgraf+updated%3A2019-02-15..2020-02-20&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AconsideRatio+updated%3A2019-02-15..2020-02-20&type=Issues) | [@databasedav](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Adatabasedav+updated%3A2019-02-15..2020-02-20&type=Issues) | [@harshu1470](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aharshu1470+updated%3A2019-02-15..2020-02-20&type=Issues) | [@hiroki-sawano](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Ahiroki-sawano+updated%3A2019-02-15..2020-02-20&type=Issues) | [@JohnPaton](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AJohnPaton+updated%3A2019-02-15..2020-02-20&type=Issues) | [@lambdaTotoro](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3AlambdaTotoro+updated%3A2019-02-15..2020-02-20&type=Issues) | [@leportella](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aleportella+updated%3A2019-02-15..2020-02-20&type=Issues) | [@meownoid](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Ameownoid+updated%3A2019-02-15..2020-02-20&type=Issues) | [@paulbaracch](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Apaulbaracch+updated%3A2019-02-15..2020-02-20&type=Issues) | [@raethlein](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Araethlein+updated%3A2019-02-15..2020-02-20&type=Issues) | [@xrdy511623](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Axrdy511623+updated%3A2019-02-15..2020-02-20&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Ayuvipanda+updated%3A2019-02-15..2020-02-20&type=Issues)

### 0.0.4 - 2019-02-15

#### Merged PRs

- Change image of block attemps workflow [#64](https://github.com/jupyterhub/nativeauthenticator/pull/64) ([@leportella](https://github.com/leportella))
- add MANIFEST.in to ensure files get packaged [#63](https://github.com/jupyterhub/nativeauthenticator/pull/63) ([@minrk](https://github.com/minrk))
- Remove duplication creation of user [#62](https://github.com/jupyterhub/nativeauthenticator/pull/62) ([@leportella](https://github.com/leportella))
- Change package_data to include_package_data [#60](https://github.com/jupyterhub/nativeauthenticator/pull/60) ([@leportella](https://github.com/leportella))
- fix raise error when email is none [#56](https://github.com/jupyterhub/nativeauthenticator/pull/56) ([@00Kai0](https://github.com/00Kai0))
- fix password is not bytes in mysql [#55](https://github.com/jupyterhub/nativeauthenticator/pull/55) ([@00Kai0](https://github.com/00Kai0))

#### Contributors to this release

[@00Kai0](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3A00Kai0+updated%3A2019-02-13..2019-02-15&type=Issues) | [@leportella](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aleportella+updated%3A2019-02-13..2019-02-15&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aminrk+updated%3A2019-02-13..2019-02-15&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Ayuvipanda+updated%3A2019-02-13..2019-02-15&type=Issues)

### 0.0.3 - 2019-02-13

#### Merged PRs

- Change package_data to include_package_data [#60](https://github.com/jupyterhub/nativeauthenticator/pull/60) ([@leportella](https://github.com/leportella))
- Increase Native Auth version to 0.0.2 [#59](https://github.com/jupyterhub/nativeauthenticator/pull/59) ([@leportella](https://github.com/leportella))

#### Contributors to this release

[@leportella](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aleportella+updated%3A2019-02-13..2019-02-13&type=Issues)

#### Merged PRs

- Change package_data to include_package_data [#60](https://github.com/jupyterhub/nativeauthenticator/pull/60) ([@leportella](https://github.com/leportella))
- Increase Native Auth version to 0.0.2 [#59](https://github.com/jupyterhub/nativeauthenticator/pull/59) ([@leportella](https://github.com/leportella))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/nativeauthenticator/graphs/contributors?from=2019-02-13&to=2019-02-13&type=c))

[@leportella](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aleportella+updated%3A2019-02-13..2019-02-13&type=Issues)

### 0.0.2 - 2019-02-13

#### Merged PRs

- Change button from Deauthorize to Unauthorize [#58](https://github.com/jupyterhub/nativeauthenticator/pull/58) ([@leportella](https://github.com/leportella))
- Add description to README and setup.py [#54](https://github.com/jupyterhub/nativeauthenticator/pull/54) ([@leportella](https://github.com/leportella))
- Fix data packaging on setup.py [#53](https://github.com/jupyterhub/nativeauthenticator/pull/53) ([@leportella](https://github.com/leportella))

#### Contributors to this release

[@leportella](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aleportella+updated%3A2019-02-12..2019-02-13&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Ayuvipanda+updated%3A2019-02-12..2019-02-13&type=Issues)

### 0.0.1 - 2019-02-12

#### Merged PRs

- Improving docs with images [#50](https://github.com/jupyterhub/nativeauthenticator/pull/50) ([@leportella](https://github.com/leportella))
- Delete user info from admin panel [#49](https://github.com/jupyterhub/nativeauthenticator/pull/49) ([@leportella](https://github.com/leportella))
- Add all info from signup post to get_or_create_user [#48](https://github.com/jupyterhub/nativeauthenticator/pull/48) ([@leportella](https://github.com/leportella))
- Fix installation errors [#46](https://github.com/jupyterhub/nativeauthenticator/pull/46) ([@leportella](https://github.com/leportella))
- Username sanitization [#43](https://github.com/jupyterhub/nativeauthenticator/pull/43) ([@leportella](https://github.com/leportella))
- Remove message decision from Signup post method [#42](https://github.com/jupyterhub/nativeauthenticator/pull/42) ([@leportella](https://github.com/leportella))
- Add email as an option to be asked on sign up [#41](https://github.com/jupyterhub/nativeauthenticator/pull/41) ([@leportella](https://github.com/leportella))
- Add endpoint for changing password [#40](https://github.com/jupyterhub/nativeauthenticator/pull/40) ([@leportella](https://github.com/leportella))
- Add option for open signup and add style to result msgs [#38](https://github.com/jupyterhub/nativeauthenticator/pull/38) ([@leportella](https://github.com/leportella))
- Add option to see password on signup [#37](https://github.com/jupyterhub/nativeauthenticator/pull/37) ([@leportella](https://github.com/leportella))
- Add check if user exceeded attempt of logins [#36](https://github.com/jupyterhub/nativeauthenticator/pull/36) ([@leportella](https://github.com/leportella))
- Improve docs [#35](https://github.com/jupyterhub/nativeauthenticator/pull/35) ([@leportella](https://github.com/leportella))
- Add missing template from authorization page [#32](https://github.com/jupyterhub/nativeauthenticator/pull/32) ([@leportella](https://github.com/leportella))
- Add password strength option [#31](https://github.com/jupyterhub/nativeauthenticator/pull/31) ([@leportella](https://github.com/leportella))
- Add admin authorization system to new users [#29](https://github.com/jupyterhub/nativeauthenticator/pull/29) ([@leportella](https://github.com/leportella))
- Add relationship between User and UserInfo [#27](https://github.com/jupyterhub/nativeauthenticator/pull/27) ([@leportella](https://github.com/leportella))
- Add authentication based on userinfo [#25](https://github.com/jupyterhub/nativeauthenticator/pull/25) ([@leportella](https://github.com/leportella))
- Add user info table [#24](https://github.com/jupyterhub/nativeauthenticator/pull/24) ([@leportella](https://github.com/leportella))
- Add new user [#16](https://github.com/jupyterhub/nativeauthenticator/pull/16) ([@leportella](https://github.com/leportella))
- Fix Circle Ci badge [#15](https://github.com/jupyterhub/nativeauthenticator/pull/15) ([@leportella](https://github.com/leportella))
- Add signup post form [#14](https://github.com/jupyterhub/nativeauthenticator/pull/14) ([@leportella](https://github.com/leportella))
- Add badges to README [#13](https://github.com/jupyterhub/nativeauthenticator/pull/13) ([@leportella](https://github.com/leportella))
- Add codecov to circle ci and requirements [#12](https://github.com/jupyterhub/nativeauthenticator/pull/12) ([@leportella](https://github.com/leportella))
- Add signup area [#11](https://github.com/jupyterhub/nativeauthenticator/pull/11) ([@leportella](https://github.com/leportella))
- Add docs link on README [#10](https://github.com/jupyterhub/nativeauthenticator/pull/10) ([@leportella](https://github.com/leportella))
- Add docs with sphinx [#9](https://github.com/jupyterhub/nativeauthenticator/pull/9) ([@leportella](https://github.com/leportella))
- Add circleci for flake8 [#7](https://github.com/jupyterhub/nativeauthenticator/pull/7) ([@leportella](https://github.com/leportella))
- Add minimal tests [#5](https://github.com/jupyterhub/nativeauthenticator/pull/5) ([@leportella](https://github.com/leportella))
- Add first structure to NativeAuthenticator [#4](https://github.com/jupyterhub/nativeauthenticator/pull/4) ([@leportella](https://github.com/leportella))

#### Contributors to this release

[@leportella](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aleportella+updated%3A2018-12-03..2019-02-12&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Aminrk+updated%3A2018-12-03..2019-02-12&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fnativeauthenticator+involves%3Ayuvipanda+updated%3A2018-12-03..2019-02-12&type=Issues)
