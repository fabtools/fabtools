"""
System services
===============

This module provides low-level tools for managing system services,
using the ``service`` command. It supports both `upstart`_ services
and traditional SysV-style ``/etc/init.d/`` scripts.

.. _upstart: http://upstart.ubuntu.com/

"""
from __future__ import with_statement

from fabric.api import *


def is_running(service):
    """
    Check if a service is running.

    ::

        import fabtools

        if fabtools.service.is_running('foo'):
            print "Service foo is running!"
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('service %(service)s status' % locals())
        return res.succeeded


def start(service):
    """
    Start a service.

    ::

        import fabtools

        # Start service if it is not running
        if not fabtools.service.is_running('foo'):
            fabtools.service.start('foo')
    """
    sudo('service %(service)s start' % locals())


def stop(service):
    """
    Stop a service.

    ::

        import fabtools

        # Stop service if it is running
        if fabtools.service.is_running('foo'):
            fabtools.service.stop('foo')
    """
    sudo('service %(service)s stop' % locals())


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
    sudo('service %(service)s restart' % locals())
