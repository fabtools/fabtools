"""
OpenSSH tasks
=============

This module provides tools to manage OpenSSH server and client.

"""

from fabric.api import hide
from fabric.contrib.files import append, sed

from fabtools.service import is_running, restart
from fabtools.files import watch


def _append(filename, regex, use_sudo):
    """
    Less verbose append
    """
    with hide('stdout', 'warnings'):
        return append(filename, regex, use_sudo=use_sudo)


_PASSWORD_AUTHENTICATION = r'^(\s*#\s*)?PasswordAuthentication\s+(yes|no)'


def disable_password_auth(sshd_config='/etc/ssh/sshd_config'):
    """
    Do not allow users to use passwords to login via ssh.
    """

    with watch(sshd_config) as config_file:

        # First try to change existing setting
        sed(sshd_config,
            _PASSWORD_AUTHENTICATION,
            'PasswordAuthentication no',
            use_sudo=True)

        # Then append setting if it's still missing
        _append(sshd_config,
                'PasswordAuthentication no',
                use_sudo=True)

    if config_file.changed and is_running('ssh'):
        restart('ssh')


def enable_password_auth(sshd_config='/etc/ssh/sshd_config'):
    """
    Allow users to use passwords to login via ssh.
    """

    with watch(sshd_config) as config_file:

        # First try to change existing setting
        sed(sshd_config,
            _PASSWORD_AUTHENTICATION,
            'PasswordAuthentication yes',
            use_sudo=True)

        # Then append setting if it's still missing
        _append(sshd_config,
                'PasswordAuthentication yes',
                use_sudo=True)

    if config_file.changed and is_running('ssh'):
        restart('ssh')


_PERMIT_ROOT_LOGIN = r'^(\s*#\s*)?PermitRootLogin\s+(yes|no)'


def disable_root_login(sshd_config='/etc/ssh/sshd_config'):
    """
    Do not allow root to login via ssh.
    """

    with watch(sshd_config) as config_file:

        # First try to change existing setting
        sed(sshd_config,
            _PERMIT_ROOT_LOGIN,
            'PermitRootLogin no',
            use_sudo=True)

        # Then append setting if it's still missing
        _append(sshd_config,
                'PermitRootLogin no',
                use_sudo=True)

    if config_file.changed and is_running('ssh'):
        restart('ssh')


def enable_root_login(sshd_config='/etc/ssh/sshd_config'):
    """
    Allow root to login via ssh.
    """

    with watch(sshd_config) as config_file:

        # First try to change existing setting
        sed(sshd_config,
            _PERMIT_ROOT_LOGIN,
            'PermitRootLogin yes',
            use_sudo=True)

        # Then append setting if it's still missing
        _append(sshd_config,
                'PermitRootLogin yes',
                use_sudo=True)

    if config_file.changed and is_running('ssh'):
        restart('ssh')


def harden(allow_root_login=False, allow_password_auth=False,
           sshd_config='/etc/ssh/sshd_config'):
    """
    Apply best practices for ssh security.

    See :func:`fabtools.ssh.disable_password_auth` and
    :func:`fabtools.ssh.disable_root_login` for a detailed
    description.

    ::

        import fabtools

        # This will apply all hardening techniques.
        fabtools.ssh.harden()

        # Only apply some of the techniques.
        fabtools.ssh.harden(allow_password_auth=True)

        # Override the sshd_config file location.
        fabtools.ssh.harden(sshd_config='/etc/sshd_config')

    """

    if not allow_password_auth:
        disable_password_auth(sshd_config=sshd_config)

    if not allow_root_login:
        disable_root_login(sshd_config=sshd_config)
