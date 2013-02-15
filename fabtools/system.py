"""
System settings
===============
"""
from __future__ import with_statement

from fabric.api import *

from fabtools.utils import run_as_root


def get_hostname():
    """
    Get the fully qualified hostname.
    """
    with settings(hide('running', 'stdout')):
        return run('hostname --fqdn')


def set_hostname(hostname, persist=True):
    """
    Set the hostname.
    """
    run_as_root('hostname %s' % hostname)
    if persist:
        run_as_root('echo %s >/etc/hostname' % hostname)


def get_sysctl(key):
    """
    Get a kernel parameter.

    Example::

        from fabtools.system import get_sysctl

        print "Max number of open files:", get_sysctl('fs.file-max')

    """
    with settings(hide('running', 'stdout')):
        return run_as_root('/sbin/sysctl -n -e %(key)s' % locals())


def set_sysctl(key, value):
    """
    Set a kernel parameter.

    Example::

        import fabtools

        # Protect from SYN flooding attack
        fabtools.system.set_sysctl('net.ipv4.tcp_syncookies', 1)

    """
    run_as_root('/sbin/sysctl -n -e -w %(key)s=%(value)s' % locals())


def supported_locales():
    """
    Gets the list of supported locales.

    Each locale is returned as a ``(locale, charset)`` tuple.
    """
    with settings(hide('running', 'stdout')):
        res = run('grep -v "^#" /usr/share/i18n/SUPPORTED')
    return [line.split(' ') for line in res.splitlines()]


def get_arch():
    """
    Get the current architecture.

    """
    with settings(hide('running', 'stdout')):
        arch = run('uname -p')
        return arch
