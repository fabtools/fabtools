"""
OpenSSH tasks
=============

This module provides tools to manage OpenSSH server and client.

"""

from fabric.contrib.files import sed


def disable_password_auth():
    """
    Do not allow users to use passwords to login via ssh.
    """

    sed('/etc/ssh/sshd_config',
        '#PasswordAuthentication yes',
        'PasswordAuthentication no',
        use_sudo=True)


def disable_root_login():
    """
    Do not allow root to login via ssh.
    """

    sed('/etc/ssh/sshd_config',
        'PermitRootLogin yes',
        'PermitRootLogin no',
        use_sudo=True)
