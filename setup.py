from setuptools import setup, find_packages
import os
from shutil import copyfile

os.rename("/usr/local/share/jupyterhub/templates/page.html", "/usr/local/share/jupyterhub/templates/jupyterhub_page.html")
copyfile("templates/page.html", "/usr/local/share/jupyterhub/templates/page.html")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jupyterhub-nativeauthenticator',
    version='0.0.4',
    description='JupyterHub Native Authenticator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jupyterhub/nativeauthenticator',
    author='Leticia Portella',
    author_email='leportella@protonmail.com',
    license='3 Clause BSD',
    packages=find_packages(),
    install_requires=['jupyterhub>=0.8', 'bcrypt', 'onetimepass'],
    include_package_data=True,
)
