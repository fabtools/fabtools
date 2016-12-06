"""
Postfix
=======

This module provides high-level tools for managing the Postfix_ email server.

.. _Postfix: http://www.postfix.org/

"""

from fabtools.deb import (
    install,
    is_installed,
    preseed_package,
)

from fabtools.require.service import started


def server(mailname):
    """
    Require a Postfix email server.

    This makes sure that Postfix is installed and started.

    ::

        from fabtools import require

        # Handle incoming email for our domain
        require.postfix.server('example.com')

    """

    # Ensure the package is installed
    if not is_installed('postfix'):
        preseed_package('postfix', {
            'postfix/main_mailer_type': ('select', 'Internet Site'),
            'postfix/mailname': ('string', mailname),
            'postfix/destinations': (
                'string', '%s, localhost.localdomain, localhost ' % mailname),
        })
        install('postfix')

    # Ensure the service is started
    started('postfix')
