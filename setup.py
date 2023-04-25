from setuptools import find_packages
from setuptools import setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="jupyterhub-nativeauthenticator",
    version="1.2.0.dev",
    description="JupyterHub Native Authenticator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jupyterhub/nativeauthenticator",
    author="Leticia Portella",
    author_email="leportella@protonmail.com",
    license="3 Clause BSD",
    packages=find_packages(),
    install_requires=["jupyterhub>=1.3", "bcrypt", "pyotp", "qrcode"],
    include_package_data=True,
)
