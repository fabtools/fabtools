"""
Idempotent API for managing services
"""
from fabric.api import *
from fabtools.service import *


def started(service):
    if not is_running(service):
        start(service)


def stopped(service):
    if is_running(service):
        stop(service)


def restarted(service):
    if is_running(service):
        restart(service)
    else:
        start(service)


__all__ = ['started', 'stopped', 'restarted']
