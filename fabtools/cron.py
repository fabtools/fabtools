"""
Cron tasks
==========

This module provides tools to manage periodic tasks using cron.

"""
from __future__ import with_statement

from tempfile import NamedTemporaryFile

from fabric.api import *
from fabtools.files import upload_template


def add_task(name, timespec, user, command):
    """
    Add a cron task.

    The *command* will be run as *user* periodically.

    You can use any valid `crontab(5)`_ *timespec*, including the
    ``@hourly``, ``@daily``, ``@weekly``, ``@monthly`` and ``@yearly``
    shortcuts.

    Examples::

        from fabtools.cron import add_task

        # Run every month
        add_task('cleanup', '@monthly', 'alice', '/home/alice/bin/cleanup.sh')

        # Run every tuesday and friday at 5:30am
        add_task('reindex', '30 5 * * 2,4', 'bob', '/home/bob/bin/reindex.sh')

    .. _crontab(5): http://manpages.debian.net/cgi-bin/man.cgi?query=crontab&sektion=5

    """
    with NamedTemporaryFile() as script:
        script.write('%(timespec)s %(user)s %(command)s\n' % locals())
        script.flush()
        upload_template('/etc/cron.d/%(name)s' % locals(),
            script.name,
            context={},
            chown=True,
            use_sudo=True)


def add_daily(name, user, command):
    """
    Shortcut to add a daily cron task.

    Example::

        import fabtools

        # Run every day
        fabtools.cron.add_daily('backup', 'root', '/usr/local/bin/backup.sh')

    """
    add_task(name, '@daily', user, command)
