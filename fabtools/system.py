"""
Fabric tools for managing system settings
"""

from fabric.api import *


def get_hostname():
    """
    Get the fully qualified hostname
    """
    with settings(hide('running', 'stdout')):
        return run('hostname --fqdn')


def set_hostname(hostname, persist=True):
    """
    Set the hostname
    """
    sudo('hostname %s' % hostname)
    if persist:
        sudo('echo %s >/etc/hostname' % hostname)


def get_sysctl(key):
    """
    Get a kernel parameter
    """
    with settings(hide('running', 'stdout')):
        return sudo('/sbin/sysctl -n -e %(key)s' % locals())


def set_sysctl(key, value):
    """
    Set a kernel parameter
    """
    sudo('/sbin/sysctl -n -e -w %(key)s=%(value)s' % locals())
