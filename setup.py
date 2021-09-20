from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jupyterhub-nativeauthenticator',
    version='0.0.7',
    description='JupyterHub Native Authenticator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jupyterhub/nativeauthenticator',
    author='Leticia Portella',
    author_email='leportella@protonmail.com',
    license='3 Clause BSD',
    packages=find_packages(),
    install_requires=['jupyterhub>=1.3', 'bcrypt', 'onetimepass'],
    include_package_data=True,
)
