"""
Systemd services
================

This module provides low-level tools for managing `systemd`_ services.

.. _systemd: http://www.freedesktop.org/wiki/Software/systemd

"""

from fabric.api import hide, settings

from fabtools.utils import run_as_root


def action(action, service):
    return run_as_root('systemctl %s %s.service' % (action, service,))


def enable(service):
    """
    Enable a service.

    ::

        fabtools.enable('httpd')

    .. note:: This function is idempotent.
    """
    action('enable', service)


def disable(service):
    """
    Disable a service.

    ::

        fabtools.systemd.disable('httpd')

    .. note:: This function is idempotent.
    """
    action('disable', service)


def is_running(service):
    """
    Check if a service is running.

    ::

        if fabtools.systemd.is_running('httpd'):
            print("Service httpd is running!")
    """
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        return action('status', service).succeeded


def start(service):
    """
    Start a service.

    ::

        if not fabtools.systemd.is_running('httpd'):
            fabtools.systemd.start('httpd')

    .. note:: This function is idempotent.
    """
    action('start', service)


def stop(service):
    """
    Stop a service.

    ::

        if fabtools.systemd.is_running('foo'):
            fabtools.systemd.stop('foo')

    .. note:: This function is idempotent.
    """
    action('stop', service)


def restart(service):
    """
    Restart a service.

    ::

        if fabtools.systemd.is_running('httpd'):
            fabtools.systemd.restart('httpd')
        else:
            fabtools.systemd.start('httpd')
    """
    action('restart', service)


def reload(service):
    """
    Reload a service.

    ::

        fabtools.systemd.reload('foo')

    .. warning::

        The service needs to support the ``reload`` operation.
    """
    action('reload', service)


def start_and_enable(service):
    """
    Start and enable a service (convenience function).

    .. note:: This function is idempotent.
    """
    start(service)
    enable(service)


def stop_and_disable(service):
    """
    Stop and disable a service (convenience function).

    .. note:: This function is idempotent.
    """
    stop(service)
    disable(service)
