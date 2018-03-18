"""
CRUX Linux packages
===================

This module provides high-level tools for managing CRUX Linux packages
and repositories.
"""

from __future__ import with_statement

from fabtools.crux import (
    install,
    is_installed,
    uninstall,
)


def package(name, update=False):
    """
    Require an CRUX Linux package to be installed.

    Example::

        from fabtools import require

        require.crux.package("foo")
    """

    if not is_installed(name):
        install(name, update)


def packages(packages, update=False):
    """
    Require several CRUX Linux packages to be installed.

    Example::

        from fabtools import require

        require.crux.packages([
            "foo",
            "bar",
            "baz",
        ])
    """

    packages = [pkg for pkg in packages if not is_installed(pkg)]

    if packages:
        install(packages, update)


def nopackage(name):
    """
    Require an CRUX Linux package to be uninstalled.

    Example::

        from fabtools import require

        require.crux.nopackage("apache2")
    """

    if is_installed(name):
        uninstall(name)


def nopackages(packages):
    """
    Require several CRUX Linux packages to be uninstalled.

    Example::

        from fabtools import require

        require.crux.nopackages([
            "perl",
            "php5",
            "ruby",
        ])
    """

    packages = [pkg for pkg in packages if is_installed(pkg)]

    if packages:
        uninstall(packages)
