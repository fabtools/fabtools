"""
Fabric tools for managing crontab tasks
"""
from __future__ import with_statement

from tempfile import NamedTemporaryFile

from fabric.api import *
from fabtools.files import upload_template


def add_task(name, timespec, user, command):
    """
    Add a cron task
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
    Add a cron task to run daily
    """
    add_task(name, '@daily', user, command)
