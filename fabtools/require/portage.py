# -*- coding: utf-8 -*-
"""
Gentoo packages
===============

This module provides high-level tools for managing Gentoo packages
and repositories using the Portage_ package manager.

.. _Portage: http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=2&chap=1

"""

from fabtools.portage import (
    install,
    is_installed,
    uninstall,
)


def package(pkg_name, update=False):
    """
    Require a Portage package to be installed.

    Example::

        from fabtools import require

        require.portage.package('foo')
    """
    if not is_installed(pkg_name):
        install(pkg_name, update)


def packages(pkg_list, update=False):
    """
    Require several Portage packages to be installed.

    Example::

        from fabtools import require

        require.portage.packages([
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
    Require a Portage package to be uninstalled.

    Example::

        from fabtools import require

        require.portage.nopackage('apache2')
    """
    if is_installed(pkg_name):
        uninstall(pkg_name)


def nopackages(pkg_list):
    """
    Require several Portage packages to be uninstalled.

    Example::

        from fabtools import require

        require.portage.nopackages([
            'perl',
            'php5',
            'ruby',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if is_installed(pkg)]
    if pkg_list:
        uninstall(pkg_list)
