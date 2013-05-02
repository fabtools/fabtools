"""
Archlinux packages
==================

This module provides tools to manage Archlinux packages
and repositories.

"""
from __future__ import with_statement

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root


MANAGER = 'LC_ALL=C pacman'


def update_index(quiet=True):
    """
    Update pacman package definitions.
    """

    manager = MANAGER
    if quiet:
        with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
            run_as_root("%(manager)s -Sy" % locals())
    else:
        run_as_root("%(manager)s -Sy" % locals())


def upgrade():
    """
    Upgrade all packages.
    """
    manager = MANAGER
    run_as_root("%(manager)s -Su" % locals(), pty=False)


def is_installed(pkg_name):
    """
    Check if a package is installed.
    """

    manager = MANAGER
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("%(manager)s -Q %(pkg_name)s" % locals())
        return res.succeeded


def install(packages, update=False, options=None):
    """
    Install one or more packages.

    If *update* is ``True``, the package definitions will be updated
    first, using :py:func:`~fabtools.arch.update_index`.

    Extra *options* may be passed to ``pacman`` if necessary.

    Example::

        import fabtools

        # Update index, then install a single package
        fabtools.arch.install('mongodb', update=True)

        # Install multiple packages
        fabtools.arch.install([
            'mongodb',
            'python-pymongo',
        ])

    """
    manager = MANAGER
    if update:
        update_index()
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options.append("-q")
    options = " ".join(options)
    cmd = '%(manager)s -S %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)


def uninstall(packages, options=None):
    """
    Remove one or more packages.

    Extra *options* may be passed to ``pacman`` if necessary.
    """
    manager = MANAGER
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = " ".join(options)
    cmd = '%(manager)s -R %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)
