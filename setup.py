from setuptools import setup, find_packages

setup(
    name='jupyterhub-nativeauthenticator',
    version='0.0.1',
    description='JupyterHub Native Authenticator',
    url='https://github.com/jupyterhub/nativeauthenticator',
    author='Leticia Portella',
    author_email='leportella@protonmail.com',
    license='3 Clause BSD',
    packages=find_packages(),
    install_requires=['jupyterhub>=0.8', 'bcrypt'],
    package_data={
        '': ['*.html', 'common-credentials.txt'],
    }
)
