"""
Supervisor processes
====================

This module provides high-level tools for managing long-running
processes using `supervisord`_.

.. _supervisord: http://supervisord.org/

"""
from __future__ import with_statement

from fabric.api import *


def reload_config():
    """
    Reload supervisor configuration.
    """
    sudo("supervisorctl reload")


def update_config():
    """
    Reread and update supervisor job configurations.

    Less heavy-handed than a full reload, as it doesn't restart the
    backend supervisor process and all managed processes.
    """
    sudo("supervisorctl update")


def process_status(name):
    """
    Get the status of a supervisor process.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo("supervisorctl status %(name)s" % locals())
        if res.startswith("No such process"):
            return None
        else:
            return res.split()[1]


def start_process(name):
    """
    Start a supervisor process
    """
    sudo("supervisorctl start %(name)s" % locals())


def stop_process(name):
    """
    Stop a supervisor process
    """
    sudo("supervisorctl stop %(name)s" % locals())


def restart_process(name):
    """
    Restart a supervisor process
    """
    sudo("supervisorctl restart %(name)s" % locals())
