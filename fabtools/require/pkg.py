"""
SmartOS packages
================

This module provides high-level tools to manage `SmartOS`_ packages.

.. _SmartOS: http://smartos.org/

"""

from fabtools.pkg import (
    install,
    is_installed,
    uninstall,
)


def package(pkg_name, update=False, yes=None):
    """
    Require a SmartOS package to be installed.

    ::

        from fabtools import require

        require.pkg.package('foo')
    """
    if not is_installed(pkg_name):
        install(pkg_name, update, yes)


def packages(pkg_list, update=False):
    """
    Require several SmartOS packages to be installed.

    ::

        from fabtools import require

        require.pkg.packages([
            'top',
            'unzip',
            'zip',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    if pkg_list:
        install(pkg_list, update)


def nopackage(pkg_name, orphan=True):
    """
    Require a SmartOS package to be uninstalled.

    ::

        from fabtools import require

        require.pkg.nopackage('top')
    """
    if is_installed(pkg_name):
        uninstall(pkg_name, orphan)


def nopackages(pkg_list, orphan=True):
    """
    Require several SmartOS packages to be uninstalled.

    ::

        from fabtools import require

        require.pkg.nopackages([
            'top',
            'zip',
            'unzip',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if is_installed(pkg)]
    if pkg_list:
        uninstall(pkg_list, orphan)
