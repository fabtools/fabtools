"""
Arch Linux packages
===================

This module provides tools to manage Arch Linux packages
and repositories.

"""

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root


def pkg_manager():
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        output = run('which yaourt', warn_only=True)
        if output.succeeded:
            manager = 'yaourt'
        else:
            manager = 'pacman'

        return 'LC_ALL=C %s' % manager


def update_index(quiet=True):
    """
    Update pacman package definitions.
    """

    manager = pkg_manager()
    if quiet:
        with settings(
                hide('running', 'stdout', 'stderr', 'warnings'),
                warn_only=True):
            run_as_root("%(manager)s -Sy" % locals())
    else:
        run_as_root("%(manager)s -Sy" % locals())


def upgrade():
    """
    Upgrade all packages.
    """
    manager = pkg_manager()
    run_as_root("%(manager)s -Su" % locals(), pty=False)


def is_installed(pkg_name):
    """
    Check if an Arch Linux package is installed.
    """

    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("pacman -Q %(pkg_name)s" % locals())
        return res.succeeded


def install(packages, update=False, options=None):
    """
    Install one or more Arch Linux packages.

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
    manager = pkg_manager()
    if update:
        update_index()
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = " ".join(options)
    cmd = '%(manager)s -S %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)


def uninstall(packages, options=None):
    """
    Remove one or more Arch Linux packages.

    Extra *options* may be passed to ``pacman`` if necessary.
    """
    manager = pkg_manager()
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = " ".join(options)
    cmd = '%(manager)s -R %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)
