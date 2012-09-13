"""
MySQL
=====

This module provides high-level tools for installing a MySQL server
and creating MySQL users and databases.

"""
from __future__ import with_statement

from fabtools.mysql import *
from fabtools.deb import is_installed, preseed_package
from fabtools.require.deb import package
from fabtools.require.service import started


def server(version=None, password=None):
    """
    Require a MySQL server to be installed and running.

    Example::

        from fabtools import require

        require.mysql.server(password='s3cr3t')

    """
    if version:
        pkg_name = 'mysql-server-%s' % version
    else:
        pkg_name = 'mysql-server'

    if not is_installed(pkg_name):
        if password is None:
            password = prompt_password()

        with settings(hide('running')):
            preseed_package('mysql-server', {
                'mysql-server/root_password': ('password', password),
                'mysql-server/root_password_again': ('password', password),
            })

        package(pkg_name)

    started('mysql')


def user(name, password, **kwargs):
    """
    Require a MySQL user.

    Extra arguments will be passed to :py:func:`fabtools.mysql.create_user`.

    Example::

        from fabtools import require

        require.mysql.user('dbuser', 'somerandomstring')

    """
    if not user_exists(name, **kwargs):
        create_user(name, password, **kwargs)


def database(name, **kwargs):
    """
    Require a MySQL database.

    Extra arguments will be passed to :py:func:`fabtools.mysql.create_database`.

    Example::

        from fabtools import require

        require.mysql.database('myapp', owner='dbuser')

    """
    if not database_exists(name, **kwargs):
        create_database(name, **kwargs)
