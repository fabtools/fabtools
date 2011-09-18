"""
Idempotent API for managing PostgreSQL users and databases
"""
from fabtools.postgres import *
from fabtools.icanhaz.deb import package
from fabtools.icanhaz.service import started


def server(version='8.4'):
    """
    I can haz PostgreSQL server
    """
    package('postgresql-%s' % version)
    started('postgresql-%s' % version)


def user(name, password):
    """
    I can haz PostgreSQL user
    """
    if not user_exists(name):
        create_user(name, password)


def database(name, owner):
    """
    I can haz PostgreSQL database
    """
    if not database_exists(name):
        create_database(name, owner)
