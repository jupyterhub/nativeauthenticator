from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jupyterhub-nativeauthenticator',
    version='0.0.5',
    description='JupyterHub Native Authenticator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cashstory/nativeauthenticator',
    author='Martin DONADIEU',
    author_email='bob@cashstory.com',
    license='3 Clause BSD',
    packages=find_packages(),
    install_requires=['jupyterhub>=0.8', 'bcrypt', 'onetimepass'],
    include_package_data=True,
)
