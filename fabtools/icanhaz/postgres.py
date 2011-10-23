"""
Idempotent API for managing PostgreSQL users and databases
"""
import os.path

from fabtools.files import is_file
from fabtools.postgres import *
from fabtools.icanhaz.deb import package
from fabtools.icanhaz.service import started


def server(version='8.4'):
    """
    I can haz PostgreSQL server
    """
    package('postgresql-%s' % version)
    service = 'postgresql-%s' % version
    if not is_file(os.path.join('/etc/init.d', service)):
        service = 'postgresql'
    started(service)


def user(name, password):
    """
    I can haz PostgreSQL user
    """
    if not user_exists(name):
        create_user(name, password)


def database(name, owner, template='template0'):
    """
    I can haz PostgreSQL database
    """
    if not database_exists(name):
        create_database(name, owner, template)
