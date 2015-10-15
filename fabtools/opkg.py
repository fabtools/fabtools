"""
opkg packages
=============

This module provides tools to manage opkg packages
and repositories.

"""

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root


MANAGER = 'opkg'


def update_index(quiet=True):
    """
    Update opkg package definitions.
    """
    options = "--verbosity=0" if quiet else ""
    run_as_root("%s %s update" % (MANAGER, options))


def upgrade():
    """
    Upgrade all packages.
    """
    manager = MANAGER
    cmd = 'upgrade'
    run_as_root("%(manager)s %(cmd)s" % locals(), pty=False)


def is_installed(pkg_name):
    """
    Check if a package is installed.
    """
    manager = MANAGER
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("%(manager)s  status %(pkg_name)s" % locals())
        return len(res) > 0


def install(packages, update=False, options=None):
    """
    Install one or more packages.

    If *update* is ``True``, the package definitions will be updated
    first, using :py:func:`~fabtools.opkg.update_index`.

    Extra *options* may be passed to ``opkg`` if necessary.

    Example::

        import fabtools

        # Update index, then install a single package
        fabtools.opkg.install('build-essential', update=True)

        # Install multiple packages
        fabtools.opkg.install([
            'mc',
            'htop',
        ])


    """
    manager = MANAGER
    if update:
        update_index()
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options.append("--verbosity=0")
    options = " ".join(options)
    cmd = '%(manager)s install %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)


def uninstall(packages, options=None):
    """
    Remove one or more packages.

    Extra *options* may be passed to ``opkg`` if necessary.
    """
    manager = MANAGER
    command = "remove"
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = " ".join(options)
    cmd = '%(manager)s %(command)s %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)
