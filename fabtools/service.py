"""
System services
===============

This module provides low-level tools for managing system services,
using the ``service`` command. It supports both `upstart`_ services
and traditional SysV-style ``/etc/init.d/`` scripts.

.. _upstart: http://upstart.ubuntu.com/

"""

from fabric.api import hide, settings

from fabtools import systemd
from fabtools.system import using_systemd, distrib_family
from fabtools.utils import run_as_root


def is_running(service):
    """
    Check if a service is running.

    ::

        import fabtools

        if fabtools.service.is_running('foo'):
            print "Service foo is running!"
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'),
                  warn_only=True):
        if using_systemd():
            return systemd.is_running(service)
        else:
            if distrib_family() != "gentoo":
                test_upstart = run_as_root('test -f /etc/init/%s.conf' %
                                           service)
                status = _service(service, 'status')
                if test_upstart.succeeded:
                    return 'running' in status
                else:
                    return status.succeeded
            else:
                # gentoo
                status = _service(service, 'status')
                return ' started' in status


def start(service):
    """
    Start a service.

    ::

        import fabtools

        # Start service if it is not running
        if not fabtools.service.is_running('foo'):
            fabtools.service.start('foo')
    """
    _service(service, 'start')


def stop(service):
    """
    Stop a service.

    ::

        import fabtools

        # Stop service if it is running
        if fabtools.service.is_running('foo'):
            fabtools.service.stop('foo')
    """
    _service(service, 'stop')


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
    _service(service, 'restart')


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
    _service(service, 'reload')


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
    _service(service, 'force-reload')


def _service(service, action):
    """
    Compatibility layer for distros that use ``service`` and those that don't.
    """
    if distrib_family() != "gentoo":
        status = run_as_root('service %(service)s %(action)s' % locals(),
                             pty=False)
    else:
        # gentoo
        status = run_as_root('/etc/init.d/%(service)s %(action)s' % locals(),
                             pty=False)
    return status
