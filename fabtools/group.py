"""
Groups
======
"""

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root


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
        args.append('-g %s' % gid)
    args.append(name)
    args = ' '.join(args)
    run_as_root('groupadd %s' % args)
