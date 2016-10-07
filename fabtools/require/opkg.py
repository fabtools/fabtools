"""
opkg packages
===============

This module provides high-level tools for managing opkg packages
and repositories.

"""

from fabtools.opkg import (
    install,
    is_installed,
    uninstall,
)


def package(pkg_name, update=False):
    """
    Require a opkg package to be installed.

    Example::

        from fabtools import require

        # Require a package
        require.opkg.package('foo')

    """
    if not is_installed(pkg_name):
        install(pkg_name, update=update)


def packages(pkg_list, update=False):
    """
    Require several opkg packages to be installed.

    Example::

        from fabtools import require

        require.opkg.packages([
            'foo',
            'bar',
            'baz',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    if pkg_list:
        install(pkg_list, update)


def nopackage(pkg_name):
    """
    Require a opkg package to be uninstalled.

    Example::

        from fabtools import require

        require.opkg.nopackage('apache2')
    """
    if is_installed(pkg_name):
        uninstall(pkg_name)


def nopackages(pkg_list):
    """
    Require several opkg packages to be uninstalled.

    Example::

        from fabtools import require

        require.opkg.nopackages([
            'perl',
            'php5',
            'ruby',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if is_installed(pkg)]
    if pkg_list:
        uninstall(pkg_list)
