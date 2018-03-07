"""
Shutdown/poweroff
========
"""

from fabric.api import hide, run, settings, sudo
from fabtools.utils import read_lines, run_as_root

def now():
    with settings(hide('running', 'stdout')):
        """
        Example::
            import fabtools
            fabtools.poweroff.now()
            OR
            fabtools.poweroff.reboot()
        """

        run_as_root('/sbin/shutdown --poweroff')

def reboot():
    with settings(hide('running', 'stdout')):
        run_as_root('/sbin/shutdown -r')
