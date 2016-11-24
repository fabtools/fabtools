# -*- coding: utf-8 -*-
"""
Gentoo packages
===============

This module provides tools for managing Gentoo packages and repositories
using the Portage_ package manager.

.. _Portage: http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=2&chap=1

"""

import re

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root


MANAGER = 'emerge --color n'


def update_index(quiet=True):
    """
    Update Portage package definitions.
    """
    manager = MANAGER

    if quiet:
        with settings(hide('running', 'stdout', 'stderr', 'warnings'),
                      warn_only=True):
            run_as_root("%(manager)s --sync" % locals())
    else:
        run_as_root("%(manager)s --sync" % locals())


def is_installed(pkg_name):
    """
    Check if a Portage package is installed.
    """
    manager = MANAGER

    with settings(hide("running", "stdout", "stderr", "warnings"),
                  warn_only=True):
        res = run("%(manager)s -p %(pkg_name)s" % locals())

    if not res.succeeded:
        return False

    if pkg_name.startswith("="):
        # The =, which is required when installing/checking for absolute
        # versions, will not appear in the results.
        pkg_name = pkg_name[1:]

    match = re.search(
        r"\n\[ebuild +(?P<code>\w+) *\] .*%(pkg_name)s.*" % locals(),
        res.stdout)
    if match and match.groupdict()["code"] in ("U", "R"):
        return True
    else:
        return False


def install(packages, update=False, options=None):
    """
    Install one or more Portage packages.

    If *update* is ``True``, the package definitions will be updated
    first, using :py:func:`~fabtools.portage.update_index`.

    Extra *options* may be passed to ``emerge`` if necessary.

    Example::

        import fabtools

        # Update index, then install a single package
        fabtools.portage.install('mongodb', update=True)

        # Install multiple packages
        fabtools.arch.install([
            'dev-db/mongodb',
            'pymongo',
        ])

    """
    manager = MANAGER

    if update:
        update_index()

    options = options or []
    options = " ".join(options)

    if not isinstance(packages, basestring):
        packages = " ".join(packages)

    cmd = '%(manager)s %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)


def uninstall(packages, options=None):
    """
    Remove one or more Portage packages.

    Extra *options* may be passed to ``emerge`` if necessary.
    """
    manager = MANAGER

    options = options or []
    options = " ".join(options)

    if not isinstance(packages, basestring):
        packages = " ".join(packages)

    cmd = '%(manager)s --unmerge %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)
