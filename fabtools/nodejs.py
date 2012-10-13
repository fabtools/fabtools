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


def install_nodejs(version=DEFAULT_VERSION):
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


def install(package=None, version=None, local=False):
    """
    Install Node.js package using ``npm``.

    If *local* is ``True``, the package will be installed locally.

    ::

        import fabtools

        # Install package globally
        fabtools.nodejs.install('express')

        # Install package locally
        fabtools.nodejs.install('underscore', local=False)

    If no package name is given, then ``npm install`` will be run,
    which will locally install all packages specified in the
    ``package.json`` file in the current directory.
    """
    if package:
        if version:
            package += '@%s' % version

        if local:
            run('npm install -l %s' % package)
        else:
            sudo('HOME=/root npm install -g %s' % package)
    else:
        run('npm install')


def update(package, local=False):
    """
    Update Node.js package.

    If *local* is ``True``, the package will be updated locally.
    """
    if local:
        run('npm update -l %s' % package)
    else:
        sudo('HOME=/root npm update -g %s' % package)


def uninstall(package, version=None, local=False):
    """
    Uninstall Node.js package.

    If *local* is ``True``, the package will be uninstalled locally.

    ::

        import fabtools

        # Uninstall package globally
        fabtools.nodejs.uninstall('express')

        # Uninstall package locally
        fabtools.nodejs.uninstall('underscore', local=False)

    """
    if version:
        package += '@%s' % version

    if local:
        run('npm uninstall -l %s' % package)
    else:
        sudo('HOME=/root npm uninstall -g %s' % package)
