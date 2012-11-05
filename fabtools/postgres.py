"""
PostgreSQL users and databases
==============================

This module provides tools for creating PostgreSQL users and databases.

"""
from __future__ import with_statement

from fabric.api import *


def _run_as_pg(command):
    """
    Run command as 'postgres' user
    """
    with cd('/var/lib/postgresql'):
        return sudo('sudo -u postgres %s' % command)


def user_exists(name):
    """
    Check if a PostgreSQL user exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = _run_as_pg('''psql -t -A -c "SELECT COUNT(*) FROM pg_user WHERE usename = '%(name)s';"''' % locals())
    return (res == "1")


def create_user(name, password, options=None):
    """
    Create a PostgreSQL user.

    Example::

        import fabtools

        # Create DB user if it does not exist
        if not fabtools.postgres.user_exists('dbuser'):
            fabtools.postgres.create_user('dbuser', password='somerandomstring')

    """
    o = {
        'SUPERUSER': False,
        'CREATEDB': False,
        'CREATEROLE': False,
        'INHERIT': True,
        'LOGIN': True,
        'CONNECTION_LIMIT': None,
        'ENCRYPTED_PASSWORD': False,
    }
    if options is not None:
        o.update(options)
    parts = [
        'psql -c "',
        'CREATE USER %s ' % (name,),
        o.get('SUPERUSER') and 'SUPERUSER ' or 'NOSUPERUSER ',
        o.get('CREATEDB') and 'CREATEDB ' or 'NOCREATEDB ',
        o.get('CREATEROLE') and 'CREATEROLE ' or 'NOCREATEROLE ',
        o.get('INHERIT') and 'INHERIT ' or 'NOINHERIT ',
        o.get('LOGIN') and 'LOGIN ' or 'NOLOGIN ',
        (o.get('CONNECTION_LIMIT')
         and 'CONNECTION LIMIT %d ' % (o.get('CONNECTION_LIMIT'),)
         or ''),
        o.get('ENCRYPTED_PASSWORD') and 'ENCRYPTED ' or '',
        '''PASSWORD '%s';''' % (password,),
        '"',
    ]
    command = ''.join(parts)
    _run_as_pg(command)


def database_exists(name):
    """
    Check if a PostgreSQL database exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        return _run_as_pg('''psql -d %(name)s -c ""''' % locals()).succeeded


def create_database(name, owner, template='template0', encoding='UTF8', locale='en_US.UTF-8'):
    """
    Create a PostgreSQL database.

    Example::

        import fabtools

        # Create DB if it does not exist
        if not fabtools.postgres.database_exists('myapp'):
            fabtools.postgres.create_database('myapp', owner='dbuser')

    """
    _run_as_pg('''createdb --owner %(owner)s --template %(template)s --encoding=%(encoding)s\
 --lc-ctype=%(locale)s --lc-collate=%(locale)s %(name)s''' % locals())
