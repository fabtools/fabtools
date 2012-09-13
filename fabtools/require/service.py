"""
System services
===============

This module provides high-level tools for managing system services.
The underlying operations use the ``service`` command, allowing to
support both `upstart`_ services and traditional SysV-style
``/etc/init.d/`` scripts.

.. _upstart: http://upstart.ubuntu.com/

"""
from fabric.api import *
from fabtools.service import *


def started(service):
    """
    Require a service to be started.

    ::

        from fabtools import require

        require.service.started('foo')
    """
    if not is_running(service):
        start(service)


def stopped(service):
    """
    Require a service to be stopped.

    ::

        from fabtools import require

        require.service.stopped('foo')
    """
    if is_running(service):
        stop(service)


def restarted(service):
    """
    Require a service to be restarted.

    ::

        from fabtools import require

        require.service.restarted('foo')
    """
    if is_running(service):
        restart(service)
    else:
        start(service)


__all__ = ['started', 'stopped', 'restarted']
