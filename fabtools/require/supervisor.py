"""
Idempotent API for managing supervisor processes
"""
from fabtools.require import deb
from fabtools.supervisor import *


def process(name, options=None):
    """
    Require a supervisor process
    """
    deb.package('supervisor')
    add_process(name, options)
    reload_config()
    if process_status(name) == 'STOPPED':
        start_process(name)
