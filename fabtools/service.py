"""
Fabric tools for managing Debian/Ubuntu packages
"""
from __future__ import with_statement

from fabric.api import *


def is_running(service):
    """
    Check if a service is running
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('/etc/init.d/%(service)s status' % locals())
        return res.succeeded


def start(service):
    """
    Start a service
    """
    sudo('/etc/init.d/%(service)s start' % locals())


def stop(service):
    """
    Stop a service
    """
    sudo('/etc/init.d/%(service)s stop' % locals())


def restart(service):
    """
    Restart a service
    """
    sudo('/etc/init.d/%(service)s restart' % locals())
