"""
Fabric tools for managing system settings
"""
from __future__ import with_statement

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


def supported_locales():
    """
    Gets the list of supported locales

    Each locale is returned as a (locale, charset) tuple
    """
    with settings(hide('running', 'stdout')):
        res = run('grep -v "^#" /usr/share/i18n/SUPPORTED')
    return [line.split(' ') for line in res.splitlines()]
