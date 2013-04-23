"""
Archlinux packages
===============

This module provides tools to manage Archlinux packages
and repositories.

"""
from __future__ import with_statement

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root


MANAGER = 'LC_ALL=C pacman'


def update_index(quiet=True, yaourt=False):
    """
    Update pacman package definitions.
    """

    manager = MANAGER
    if quiet:
        with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
            run_as_root("%(manager)s -Sy" % locals())
    else:
        run_as_root("%(manager)s -Sy" % locals())


def upgrade(yaourt=False):
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
        if res.return_code == 0:
            return True
        return False


def install(packages, update=False, yaourt=False, options=None):
    """
    Install one or more packages.

    If *update* is ``True``, the package definitions will be updated
    first, using :py:func:`~fabtools.arch.update_index`.

    Extra *options* may be passed to ``pacman`` if necessary.

    Example::

        import fabtools

        # Update index, then install a single package
        fabtools.deb.install('build-essential', update=True)

        # Install multiple packages
        fabtools.arch.install([
            'python-dev',
            'libxml2-dev',
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


def uninstall(packages, yaourt=False, options=None):
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
