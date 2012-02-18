"""
Idempotent API for managing MySQL users and databases
"""
from __future__ import with_statement

from fabtools.mysql import *
from fabtools.deb import is_installed, preseed_package
from fabtools.require.deb import package
from fabtools.require.service import started


def server(version='5.1', password=None):
    """
    Require a MySQL server
    """
    if not is_installed("mysql-server-%s" % version):
        if password is None:
            password = prompt_password()

        with settings(hide('running')):
            preseed_package('mysql-server', {
                'mysql-server/root_password': ('password', password),
                'mysql-server/root_password_again': ('password', password),
            })

        package('mysql-server-%s' % version)

    started('mysql')


def user(name, password, **kwargs):
    """
    Require a MySQL user
    """
    if not user_exists(name, **kwargs):
        create_user(name, password, **kwargs)


def database(name, **kwargs):
    """
    Require a MySQL database
    """
    if not database_exists(name, **kwargs):
        create_database(name, **kwargs)
