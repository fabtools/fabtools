"""
Idempotent API for managing MySQL users and databases
"""
from fabric.utils import warn

from fabtools.mysql import *
from fabtools.deb import preseed_package
from fabtools.icanhaz.deb import package
from fabtools.icanhaz.service import started


def server(version='5.1'):
    """
    I can haz MySQL server
    """
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show mysql-server')

    if result.failed is False:
        warn('MySQL is already installed')
    else:
        mysql_password = prompt_password()

        preseed_package('mysql-server', {
            'mysql-server/root_password': ('password', mysql_password),
            'mysql-server/root_password_again': ('password', mysql_password),
        })

        package('mysql-server-%s' % version)

    started('mysql')

def user(name, passwd, **options):
    """
    I can haz MySQL user
    """
    if not user_exists(name, **options):
        create_user(name, passwd, **options)


def database(name, **options):
    """
    I can haz MySQL database
    """
    if not database_exists(name, **options):
        create_database(name, **options)
