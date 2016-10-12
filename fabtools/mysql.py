"""
MySQL users and databases
=========================

This module provides tools for creating MySQL users and databases.

"""

from pipes import quote

from fabric.api import env, hide, puts, run, settings

from fabtools.utils import run_as_root


def query(query, use_sudo=True, **kwargs):
    """
    Run a MySQL query.
    """
    func = use_sudo and run_as_root or run

    user = kwargs.get('mysql_user') or env.get('mysql_user')
    password = kwargs.get('mysql_password') or env.get('mysql_password')
    mysql_host = kwargs.get('mysql_host') or env.get('mysql_host')

    options = [
        '--batch',
        '--raw',
        '--skip-column-names',
    ]
    if user:
        options.append('--user=%s' % quote(user))
    if password:
        options.append('--password=%s' % quote(password))
    if mysql_host:
        options.append('--host=%s' % quote(mysql_host))
    options = ' '.join(options)

    return func('mysql %(options)s --execute=%(query)s' % {
        'options': options,
        'query': quote(query),
    })


def user_exists(name, host='localhost', **kwargs):
    """
    Check if a MySQL user exists.
    """
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = query("""
            use mysql;
            SELECT COUNT(*) FROM user
                WHERE User = '%(name)s' AND Host = '%(host)s';
            """ % {'name': name, 'host': host}, **kwargs)
    return res.succeeded and (int(res) == 1)


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
        query(
            "CREATE USER '%(name)s'@'%(host)s' IDENTIFIED BY '%(password)s';" %
            {
                'name': name,
                'password': password,
                'host': host
            }, **kwargs)
    puts("Created MySQL user '%s'." % name)


def database_exists(name, **kwargs):
    """
    Check if a MySQL database exists.
    """
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = query("SHOW DATABASES LIKE '%(name)s';" % {
            'name': name
        }, **kwargs)

    return res.succeeded and (res == name)


def create_database(name, owner=None, owner_host='localhost', charset='utf8',
                    collate='utf8_general_ci', **kwargs):
    """
    Create a MySQL database.

    Example::

        import fabtools

        # Create DB if it does not exist
        if not fabtools.mysql.database_exists('myapp'):
            fabtools.mysql.create_database('myapp', owner='dbuser')

    """
    with settings(hide('running')):

        query("CREATE DATABASE %(name)s CHARACTER SET %(charset)s COLLATE %(collate)s;" % {
            'name': name,
            'charset': charset,
            'collate': collate
        }, **kwargs)

        if owner:
            query("GRANT ALL PRIVILEGES ON %(name)s.* TO '%(owner)s'@'%(owner_host)s' WITH GRANT OPTION;" % {
                'name': name,
                'owner': owner,
                'owner_host': owner_host
            }, **kwargs)

    puts("Created MySQL database '%s'." % name)
