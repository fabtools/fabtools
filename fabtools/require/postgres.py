"""
Idempotent API for managing PostgreSQL users and databases
"""
from __future__ import with_statement

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
        pkg_name = 'postgresql-%s' % version
    else:
        pkg_name = 'postgresql'
    package(pkg_name)

    if is_file('/etc/init.d/postgresql'):
        service_name = 'postgresql'
    else:
        if version and is_file('/etc/init.d/postgresql-%s' % version):
            service_name = 'postgresql-%s' % version
        else:
            with cd('/etc/init.d'):
                with settings(hide('running', 'stdout')):
                    service_name = run('ls postgresql-*').splitlines()[0]
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
