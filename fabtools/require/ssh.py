"""
OpenSSH
============

This module provides high-level tools for managing OpenSSH

"""
from fabtools import ssh


def harden(disable_root_login=True, disable_password_auth=True):

    """
    Apply best practices for ssh security.

    See :func:`fabtools.ssh.disable_root_login` and
    :func:`fabtools.ssh.disable_password_auth` for a detailed
    description.

    ::

        from fabtools import require

        # This will apply all hardening techniques.
        require.harden()

        # Only apply some of the techniques.
        require.ssh.harden(disable_password_auth=False)

    """

    if disable_root_login:
        ssh.disable_root_login()

    if disable_password_auth:
        ssh.disable_password_auth()
