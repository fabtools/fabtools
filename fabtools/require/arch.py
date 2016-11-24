"""
Arch Linux packages
===================

This module provides high-level tools for managing Arch Linux packages
and repositories.

"""

from fabtools.arch import (
    install,
    is_installed,
    uninstall,
)


def package(pkg_name, update=False):
    """
    Require an Arch Linux package to be installed.

    Example::

        from fabtools import require

        require.arch.package('foo')
    """
    if not is_installed(pkg_name):
        install(pkg_name, update)


def packages(pkg_list, update=False):
    """
    Require several Arch Linux packages to be installed.

    Example::

        from fabtools import require

        require.arch.packages([
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
    Require an Arch Linux package to be uninstalled.

    Example::

        from fabtools import require

        require.arch.nopackage('apache2')
    """
    if is_installed(pkg_name):
        uninstall(pkg_name)


def nopackages(pkg_list):
    """
    Require several Arch Linux packages to be uninstalled.

    Example::

        from fabtools import require

        require.arch.nopackages([
            'perl',
            'php5',
            'ruby',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if is_installed(pkg)]
    if pkg_list:
        uninstall(pkg_list)
