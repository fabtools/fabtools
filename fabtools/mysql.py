"""
Fabric tools for managing MySQL users and databases
"""
from fabric.api import *

def prompt_password(user='root'):
    mysql_password = prompt('Please enter MySQL %s password:' % user)

    return mysql_password

def _query(user, password, query, use_sudo=True):
    func = use_sudo and sudo or run

    return func('mysql -u %(user)s -p%(password)s -e "%(query)s"' % {
        'user': user,
        'password': password,
        'query': query
    })

def user_exists(name, **options):
    """
    Check if a MySQL user exists
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        user = options.get('user', 'root')

        password = prompt_password(user)

        res = _query(user, password, 'use mysql; SELECT * FROM user WHERE User = \'%(name)s\';' % {
            'name': name
        })

        return bool(res)

def create_user(name, passwd, **options):
    """
    Create a MySQL user
    """
    host = options.get('host', 'localhost')
    user = options.get('user', 'root')

    mysql_password = prompt_password(user)

    _query(user, mysql_password, "CREATE USER '%(name)s'@'%(host)s' IDENTIFIED BY '%(passwd)s';" % {
        'name': name,
        'passwd': passwd,
        'host': host
    })


def database_exists(name, **options):
    """
    Check if a MySQL database exists
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        user = options.get('user', 'root')

        password = prompt_password(user)

        res = _query(user, password, 'use mysql; SELECT * FROM db WHERE Db = \'%(name)s\';' % {
            'name': name
        })

    return bool(res)


def create_database(name, **options):
    """
    Create a MySQL database
    """
    user = options.get('user', 'root')
    owner = options.get('owner', None)
    owner_host = options.get('owner_host', 'localhost')
    character = options.get('character', 'utf8')
    collate = options.get('collate', 'utf8_general_ci')

    password = prompt_password(user)

    _query(user, password, "create database %(name)s character set %(character)s collate %(collate)s;" % {
        'name': name,
        'character': character,
        'collate': collate
    })

    if owner:
        _query(user, password, "grant all privileges on %(name)s.* TO '%(owner)s'@'%(owner_host)s' with grant option;" % {
            'name': name,
            'owner': owner,
            'owner_host': owner_host
        })
