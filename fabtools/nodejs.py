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


def install_nodejs(version="0.8.9"):
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

    filename = "node-v{version}.tar.gz".format(**locals())
    foldername = filename[0:-7]

    run("wget http://nodejs.org/dist/v{version}/{filename}".format(**locals()))
    run("tar -xzf {filename}".format(filename=filename))
    with cd(foldername):
        run("./configure ; make")
        sudo("make install")
    run('rm {filename} ; rm -rf {foldername}'.format(**locals()))


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
            package += "@{version}".format(version=version)

        if global_install:
            sudo("npm install -g {package}".format(package=package))
        else:
            run("npm install -l {package}".format(package=package))
    else:
        run("npm install")


def update(package, global_install=True):
    """
    Update Node.js package.
    """
    if global_install:
        sudo("npm update -g {package}".format(package=package))
    else:
        run("npm update -l {package}".format(package=package))


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
        package += "@{version}".format(version=version)

    if global_uninstall:
        sudo("npm uninstall -g {package}".format(package=package))
    else:
        sudo("npm uninstall -l {package}".format(package=package))
