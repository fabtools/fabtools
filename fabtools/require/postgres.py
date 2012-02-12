"""
Idempotent API for managing PostgreSQL users and databases
"""
import os.path

from fabtools.files import is_file
from fabtools.postgres import *
from fabtools.require.deb import package
from fabtools.require.service import started


def server(version=None):
    """
    Require a PostgreSQL server
    """
    if version:
        pkg_name = service_name = 'postgresql-%s' % version
    else:
        pkg_name = service_name = 'postgresql'
    package(pkg_name)
    if not is_file(os.path.join('/etc/init.d', service_name)):
        service_name = 'postgresql'
    started(service_name)


def user(name, password):
    """
    Require a PostgreSQL user
    """
    if not user_exists(name):
        create_user(name, password)


def database(name, owner, template='template0', encoding='UTF8',
             locale='en_US.UTF-8'):
    """
    Require a PostgreSQL database
    """
    if not database_exists(name):
        create_database(name, owner, template=template, encoding=encoding,
            locale=locale)
