"""
Node.js
=======

This module provides tools for installing `Node.js`_ and managing
packages using `npm`_.

.. note: the ``simplejson`` module is required on Python 2.5

.. _Node.js: http://nodejs.org/
.. _npm: http://npmjs.org/

"""

from fabtools import nodejs


def installed_from_source(version=nodejs.DEFAULT_VERSION):
    """
    Require Node.js to be installed from source.

    ::

        from fabtools import require

        require.nodejs.installed_from_source()

    """
    if nodejs.version() != version:
        nodejs.install_from_source(version)


def package(pkg_name, version=None, local=False):
    """
    Require a Node.js package.

    If the package is not installed, and no *version* is specified, the
    latest available version will be installed.

    If a *version* is specified, and a different version of the package
    is already installed, it will be updated to the specified version.

    If `local` is ``True``, the package will be installed locally.

    ::

        from fabtools import require

        # Install package system-wide
        require.nodejs.package('foo')

        # Install package locally
        require.nodejs.package('bar', local=True)

    """
    pkg_version = nodejs.package_version(pkg_name, local=local)
    if version:
        if pkg_version != version:
            nodejs.install_package(pkg_name, version, local=local)
    else:
        if pkg_version is None:
            nodejs.install_package(pkg_name, local=local)
