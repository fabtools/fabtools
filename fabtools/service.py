"""
System services
===============

This module provides low-level tools for managing system services,
using the ``service`` command. It supports both `upstart`_ services
and traditional SysV-style ``/etc/init.d/`` scripts.

.. _upstart: http://upstart.ubuntu.com/

"""
from __future__ import with_statement

from fabric.api import hide, settings

from fabtools.utils import run_as_root

from fabtools import systemd

from fabtools.system import using_systemd

def is_running(service):
    """
    Check if a service is running.

    ::

        import fabtools

        if fabtools.service.is_running('foo'):
            print "Service foo is running!"
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        if using_systemd():
            return systemd.is_running(service)
        else:
            test_upstart = run_as_root('test -f /etc/init/%s.conf' % service)
            status = run_as_root('service %(service)s status' % locals())
            if test_upstart.succeeded:
                return 'running' in status
            else:
                return status.succeeded


def start(service):
    """
    Start a service.

    ::

        import fabtools

        # Start service if it is not running
        if not fabtools.service.is_running('foo'):
            fabtools.service.start('foo')
    """
    run_as_root('service %(service)s start' % locals(), pty=False)


def stop(service):
    """
    Stop a service.

    ::

        import fabtools

        # Stop service if it is running
        if fabtools.service.is_running('foo'):
            fabtools.service.stop('foo')
    """
    run_as_root('service %(service)s stop' % locals())


def restart(service):
    """
    Restart a service.

    ::

        import fabtools

        # Start service, or restart it if it is already running
        if fabtools.service.is_running('foo'):
            fabtools.service.restart('foo')
        else:
            fabtools.service.start('foo')
    """
    run_as_root('service %(service)s restart' % locals(), pty=False)


def reload(service):
    """
    Reload a service.

    ::

        import fabtools

        # Reload service
        fabtools.service.reload('foo')

    .. warning::

        The service needs to support the ``reload`` operation.
    """
    run_as_root('service %(service)s reload' % locals(), pty=False)


def force_reload(service):
    """
    Force reload a service.

    ::

        import fabtools

        # Force reload service
        fabtools.service.force_reload('foo')

    .. warning::

        The service needs to support the ``force-reload`` operation.
    """
    run_as_root('service %(service)s force-reload' % locals(), pty=False)
