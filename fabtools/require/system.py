"""
Idempotent API for managing system settings
"""
from fabric.api import sudo

from fabtools.files import watch
from fabtools.system import get_hostname, set_hostname
from fabtools.system import get_sysctl, set_sysctl


def sysctl(key, value, persist=True):
    """
    Require a kernel parameter to have a specific value
    """
    if get_sysctl(key) != value:
        set_sysctl(key, value)

    if persist:
        from fabtools import require
        filename = '/etc/sysctl.d/60-%s.conf' % key
        def on_change():
            sudo('service procps start')
        with watch(filename, True, on_change):
            require.file(filename,
                contents='%(key)s = %(value)s\n' % locals(),
                use_sudo=True)


def hostname(name):
    """
    Require the hostname to have a specific value
    """
    if get_hostname() != name:
        set_hostname(name)
