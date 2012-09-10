"""
Fabric tools for managing services

This uses the ``service`` command, supporting both upstart services
and traditional SysV-style ``/etc/init.d/`` scripts.
"""
from __future__ import with_statement

from fabric.api import *


def is_running(service):
    """
    Check if a service is running
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('service %(service)s status' % locals())
        return res.succeeded


def start(service):
    """
    Start a service
    """
    sudo('service %(service)s start' % locals())


def stop(service):
    """
    Stop a service
    """
    sudo('service %(service)s stop' % locals())


def restart(service):
    """
    Restart a service
    """
    sudo('service %(service)s restart' % locals())
