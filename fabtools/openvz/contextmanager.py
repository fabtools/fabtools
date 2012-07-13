"""
Fabric tools for managing OpenVZ containers
"""
from contextlib import contextmanager

import fabric.operations


@contextmanager
def guest(name):
    """
    Context manager to run commands inside a guest container
    """

    # Monkey patch fabric's _run_command
    _orig_run_command = fabric.operations._run_command
    def my_run_command(command, *args, **kwargs):
        command = 'vzctl exec2 %s %s' % (name, command)
        kwargs.setdefault('sudo', True)
        return _orig_run_command(command, *args, **kwargs)
    fabric.operations._run_command = my_run_command

    yield

    # Monkey unpatch
    fabric.operations._run_command = _orig_run_command
