# -*- coding: utf-8 -*-
"""
Portage packages
===============

This module provides high-level tools for managing portage packages
and repositories.

"""
from __future__ import with_statement

from fabtools.portage import (
    install,
    is_installed,
    uninstall,
    update_index,
)


def package(pkg_name, update=False):
    """
    Require a portage package to be installed.

    Example::

        from fabtools import require

        require.portage.package('foo')
    """
    if not is_installed(pkg_name):
        install(pkg_name, update)


def packages(pkg_list, update=False):
    """
    Require several portage packages to be installed.

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
    Require a portage package to be uninstalled.

    Example::

        from fabtools import require

        require.portage.nopackage('apache2')
    """
    if is_installed(pkg_name):
        uninstall(pkg_name)


def nopackages(pkg_list):
    """
    Require several portage packages to be uninstalled.

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
