"""
Idempotent API for managing postfix email server
"""
from fabric.api import *
from fabtools.deb import is_installed, preseed_package, install
from fabtools.icanhaz.service import started


def server(mailname):
    """
    I can haz postfix email server
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
