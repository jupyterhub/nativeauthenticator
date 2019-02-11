import os
from setuptools import setup, find_packages

pjoin = os.path.join

setup_args = dict(
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
        'nativeauthenticator': [
            pjoin('templates', '*.html'),
            'common-credentials.txt'
        ],
    }
)


def main():
    setup(**setup_args)


if __name__ == '__main__':
    main()
