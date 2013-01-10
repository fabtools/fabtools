"""
Groups
======
"""
from __future__ import with_statement

from pipes import quote

from fabric.api import *


def exists(name):
    """
    Check if a group exists.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        return run('getent group %(name)s' % locals()).succeeded


def create(name, gid=None):
    """
    Create a new group.

    Example::

        import fabtools

        if not fabtools.group.exists('admin'):
            fabtools.group.create('admin')

    """

    args = []
    if gid:
        args.append('-g %s' % quote(gid))
    args.append(name)
    args = ' '.join(args)
    sudo('groupadd %s' % args)
