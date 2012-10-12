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

    Example::

        import fabtools

        # Install Node.js
        fabtools.nodejs.install_nodejs()

    .. note:: This function only works for recent versions of Node.js.

    """
    require.deb.packages([
        "make",
        "openssl",
        "python",
        "libssl-dev",
        "g++",
    ])

    filename = 'node-v%s.tar.gz' % version
    foldername = filename[0:-7]

    run('wget http://nodejs.org/dist/v%(version)s/%(filename)s' % locals())
    run('tar -xzf %s' % filename)
    with cd(foldername):
        run("./configure ; make")
        sudo("make install")
    run('rm %(filename)s ; rm -rf %(foldername)s' % locals())


def install(package=None, version=None, global_install=True):
    """
    Install Node.js package using ``npm``.

    If ``global_install`` is ``False``, the package will be installed
    locally.

    Example::

        import fabtools

        # Install package globally
        fabtools.nodejs.install('express')

        # Install package locally
        fabtools.nodejs.install('underscore', global_install=False)

    If no package name is given, then ``npm install`` will be run,
    which will locally install all packages specified in the
    ``package.json`` file in the current directory.
    """
    if package:
        if version:
            package += '@%s' % version

        if global_install:
            sudo('npm install -g %s' % package)
        else:
            run('npm install -l %s' % package)
    else:
        run("npm install")


def update(package, global_install=True):
    """
    Update Node.js package.
    """
    if global_install:
        sudo('npm update -g %s' % package)
    else:
        run('npm update -l %s' % package)


def uninstall(package, version=None, global_uninstall=True):
    """
    Uninstall Node.js package.

    If ``global_install`` is False, the package will be uninstalled
    locally.

    Example::

        import fabtools

        # Uninstall package globally
        fabtools.nodejs.uninstall('express')

        # Uninstall package locally
        fabtools.nodejs.uninstall('underscore', global_uninstall=False)

    """
    if version:
        package += '@%s' % version

    if global_uninstall:
        sudo('npm uninstall -g %s' % package)
    else:
        sudo('npm uninstall -l %s' % package)
