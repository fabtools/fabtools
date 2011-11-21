"""
Idempotent API for managing Postfix email server
"""
from fabric.api import *
from fabtools.deb import is_installed, preseed_package, install
from fabtools.require.service import started


def server(mailname):
    """
    Require a Postfix email server
    """

    # Ensure the package is installed
    if not is_installed('postfix'):
        preseed_package('postfix', {
            'postfix/main_mailer_type': ('select', 'Internet Site'),
            'postfix/mailname': ('string', mailname),
            'postfix/destinations': ('string', '%s, localhost.localdomain, localhost ' % mailname),
        })
        install('postfix')

    # Ensure the service is started
    started('postfix')
