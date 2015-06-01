"""
MySQL
=====

This module provides high-level tools for installing a MySQL server
and creating MySQL users and databases.

"""

from fabric.api import hide, prompt, settings

from fabtools.mysql import (
    create_database,
    create_user,
    database_exists,
    user_exists,
)
from fabtools.system import UnsupportedFamily, distrib_family

from fabtools.require.service import started


def server(version=None, password=None):
    """
    Require a MySQL server to be installed and running.

    Example::

        from fabtools import require

        require.mysql.server(password='s3cr3t')

    """
    family = distrib_family()
    if family == 'debian':
        _server_debian(version, password)
    else:
        raise UnsupportedFamily(supported=['debian'])


def _server_debian(version, password):

    from fabtools.deb import is_installed, preseed_package
    from fabtools.require.deb import package as require_deb_package

    if version:
        pkg_name = 'mysql-server-%s' % version
    else:
        pkg_name = 'mysql-server'

    if not is_installed(pkg_name):
        if password is None:
            password = prompt('Please enter password for MySQL user "root":')

        with settings(hide('running')):
            preseed_package('mysql-server', {
                'mysql-server/root_password': ('password', password),
                'mysql-server/root_password_again': ('password', password),
            })

        require_deb_package(pkg_name)

    started('mysql')


def user(name, password, **kwargs):
    """
    Require a MySQL user.

    Extra arguments will be passed to :py:func:`fabtools.mysql.create_user`.

    Example::

        from fabric.api import settings
        from fabtools import require

        with settings(mysql_user='root', mysql_password='s3cr3t'):
            require.mysql.user('dbuser', 'somerandomstring')

    """
    if not user_exists(name, **kwargs):
        create_user(name, password, **kwargs)


def database(name, **kwargs):
    """
    Require a MySQL database.

    Extra arguments will be passed to :py:func:`fabtools.mysql.create_database`.

    Example::

        from fabric.api import settings
        from fabtools import require

        with settings(mysql_user='root', mysql_password='s3cr3t'):
            require.mysql.database('myapp', owner='dbuser')

    """
    if not database_exists(name, **kwargs):
        create_database(name, **kwargs)
