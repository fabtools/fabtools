"""
Node.js
=======

This module provides tools for installing `Node.js`_ and managing
packages using `npm`_.

.. _Node.js: http://nodejs.org/
.. _npm: http://npmjs.org/

"""
from fabric.api import run, sudo, cd
from fabtools import require


DEFAULT_VERSION = '0.8.11'


def install_from_source(version=DEFAULT_VERSION):
    """
    Install Node JS from source.

    ::

        import fabtools

        # Install Node.js
        fabtools.nodejs.install_nodejs()

    .. note:: This function may not work for old versions of Node.js.

    """
    require.deb.packages([
        'build-essential',
        'python',
        'libssl-dev',
    ])

    filename = 'node-v%s.tar.gz' % version
    foldername = filename[0:-7]

    run('wget http://nodejs.org/dist/v%(version)s/%(filename)s' % locals())
    run('tar -xzf %s' % filename)
    with cd(foldername):
        run('./configure')
        run('make')
        sudo('make install')
    run('rm -rf %(filename)s %(foldername)s' % locals())


def install_package(package, version=None, local=False):
    """
    Install a Node.js package.

    If *local* is ``True``, the package will be installed locally.

    ::

        import fabtools

        # Install package globally
        fabtools.nodejs.install_package('express')

        # Install package locally
        fabtools.nodejs.install_package('underscore', local=False)

    """
    if version:
        package += '@%s' % version

    if local:
        run('npm install -l %s' % package)
    else:
        sudo('HOME=/root npm install -g %s' % package)


def install_dependencies():
    """
    Install Node.js package dependencies.

    This function calls ``npm install``, which will locally install all
    packages specified as dependencies in the ``package.json`` file
    found in the current directory.

    ::

        from fabric.api import cd
        from fabtools import nodejs

        with cd('/path/to/nodejsapp/'):
            nodejs.install_dependencies()

    """
    run('npm install')


def update_package(package, local=False):
    """
    Update a Node.js package.

    If *local* is ``True``, the package will be updated locally.
    """
    if local:
        run('npm update -l %s' % package)
    else:
        sudo('HOME=/root npm update -g %s' % package)


def uninstall_package(package, version=None, local=False):
    """
    Uninstall a Node.js package.

    If *local* is ``True``, the package will be uninstalled locally.

    ::

        import fabtools

        # Uninstall package globally
        fabtools.nodejs.uninstall_package('express')

        # Uninstall package locally
        fabtools.nodejs.uninstall_package('underscore', local=False)

    """
    if version:
        package += '@%s' % version

    if local:
        run('npm uninstall -l %s' % package)
    else:
        sudo('HOME=/root npm uninstall -g %s' % package)
