"""
Idempotent API for managing PostgreSQL users and databases
"""
import os.path

from fabtools.files import is_file
from fabtools.postgres import *
from fabtools.require.deb import package
from fabtools.require.service import started


def server(version='8.4'):
    """
    Require a PostgreSQL server
    """
    package('postgresql-%s' % version)
    service = 'postgresql-%s' % version
    if not is_file(os.path.join('/etc/init.d', service)):
        service = 'postgresql'
    started(service)


def user(name, password):
    """
    Require a PostgreSQL user
    """
    if not user_exists(name):
        create_user(name, password)


def database(name, owner, template='template0'):
    """
    Require a PostgreSQL database
    """
    if not database_exists(name):
        create_database(name, owner, template)
