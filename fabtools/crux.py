"""
CRUX Linux ports
================

This module provides tools to manage CRUX Linux ports
and repositories.
"""

from __future__ import with_statement


from fabric.api import abort, hide, run, settings


from fabtools.utils import run_as_root


def prtget():
    with settings(hide("running", "stdout", "stderr", "warnings"), warn_only=True):
        output = run("which prt-get", warn_only=True)
        if output.succeeded:
            manager = "prt-get"
        else:
            abort("CRUX Pakcager Manager `prt-get` not found!")

        return "LC_ALL=C {}".format(manager)


def ports():
    with settings(hide("running", "stdout", "stderr", "warnings"), warn_only=True):
        output = run("which ports", warn_only=True)
        if output.succeeded:
            manager = "ports"
        else:
            abort("CRUX Ports Utilities `pkgutils` not found!")

        return "LC_ALL=C {}".format(manager)


def update_ports(quiet=True):
    """
    Update all ports collections
    """

    manager = ports()
    if quiet:
        with settings(hide("running", "stdout", "stderr", "warnings"), warn_only=True):
            run_as_root("{} -u".format(manager))
    else:
        run_as_root("{} -u".format(manager))


def upgrade():
    """
    Upgrade all packages.
    """

    manager = prtget()
    run_as_root("{} sysup".format(manager), pty=False)


def is_installed(name):
    """
    Check if a CRUX package is installed.
    """

    with settings(hide("running", "stdout", "stderr", "warnings"), warn_only=True):
        res = run("prt-get listinst {}".format(name))
        return res.succeeded


def install(packages, update=False, options=None):
    """
    Install one or more CRUX Linux packages.

    If *update* is ``True``, the ports collections will be updated
    first, using :py:func:`~fabtools.crux.update_ports`.

    Extra *options* may be passed to ``prt-get`` if necessary.

    Example::

        import fabtools

        # Update index, then install a single package
        fabtools.crux.install("mongodb", update=True)

        # Install multiple packages
        fabtools.crux.install([
            "mongodb",
            "python-pymongo",
        ])
    """

    manager = prtget()

    if update:
        update_ports()

    if options is None:
        options = []

    options = " ".join(options)

    if not isinstance(packages, basestring):
        packages = " ".join(packages)

    cmd = "{} depinst {} {}".format(manager, options, packages)
    run_as_root(cmd, pty=False)


def uninstall(packages, options=None):
    """
    Remove one or more CRUX Linux packages.

    Extra *options* may be passed to ``prt-get`` if necessary.
    """

    manager = prtget()

    if options is None:
        options = []

    options = " ".join(options)

    if not isinstance(packages, basestring):
        packages = " ".join(packages)

    cmd = "{} remove {} {}".format(manager, options, packages)
    run_as_root(cmd, pty=False)
