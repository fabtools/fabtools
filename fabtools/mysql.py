"""
MySQL users and databases
=========================

This module provides tools for creating MySQL users and databases.

"""
from __future__ import with_statement

from fabric.api import *


def prompt_password(user='root'):
    """
    Ask MySQL password interactively.
    """
    return prompt('Please enter password for MySQL user "%s":' % user)


def _query(query, use_sudo=True, **kwargs):
    """
    Run a MySQL query.
    """
    func = use_sudo and sudo or run

    user = kwargs.get('mysql_user') or env.get('mysql_user')
    password = kwargs.get('mysql_password') or env.get('mysql_password')
    if user and not password:
        password = prompt_password(user)

    return func('mysql --batch --raw --skip-column-names --user=%(user)s --password=%(password)s --execute="%(query)s"' % {
        'user': user,
        'password': password,
        'query': query
    })


def user_exists(name, **kwargs):
    """
    Check if a MySQL user exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = _query("use mysql; SELECT User FROM user WHERE User = '%(name)s';" % {
            'name': name
        }, **kwargs)
    return res.succeeded and (res == name)


def create_user(name, password, host='localhost', **kwargs):
    """
    Create a MySQL user.

    Example::

        import fabtools

        # Create DB user if it does not exist
        if not fabtools.mysql.user_exists('dbuser'):
            fabtools.mysql.create_user('dbuser', password='somerandomstring')

    """
    with settings(hide('running')):
        _query("CREATE USER '%(name)s'@'%(host)s' IDENTIFIED BY '%(password)s';" % {
            'name': name,
            'password': password,
            'host': host
        }, **kwargs)
    puts("Created MySQL user '%s'." % name)


def database_exists(name, **kwargs):
    """
    Check if a MySQL database exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = _query("use mysql; SELECT Db FROM db WHERE Db = '%(name)s';" % {
            'name': name
        }, **kwargs)

    return res.succeeded and (res == name)


def create_database(name, owner=None, owner_host='localhost', charset='utf8', collate='utf8_general_ci', **kwargs):
    """
    Create a MySQL database.

    Example::

        import fabtools

        # Create DB if it does not exist
        if not fabtools.mysql.database_exists('myapp'):
            fabtools.mysql.create_database('myapp', owner='dbuser')

    """
    with settings(hide('running')):

        _query("CREATE DATABASE %(name)s CHARACTER SET %(charset)s COLLATE %(collate)s;" % {
            'name': name,
            'charset': charset,
            'collate': collate
        }, **kwargs)

        if owner:
            _query("GRANT ALL PRIVILEGES ON %(name)s.* TO '%(owner)s'@'%(owner_host)s' WITH GRANT OPTION;" % {
                'name': name,
                'owner': owner,
                'owner_host': owner_host
            }, **kwargs)

    puts("Created MySQL database '%s'." % name)
