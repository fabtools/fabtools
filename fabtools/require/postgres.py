"""
PostgreSQL users and databases
==============================
"""
from __future__ import with_statement

from fabtools.files import is_file, watch
from fabtools.postgres import *
from fabtools.require.deb import package
from fabtools.require.service import started, restarted
from fabtools.require.system import locale as require_locale


def _service_name(version=None):

    if is_file('/etc/init.d/postgresql'):
        return 'postgresql'

    if version and is_file('/etc/init.d/postgresql-%s' % version):
        return 'postgresql-%s' % version

    with cd('/etc/init.d'):
        with settings(hide('running', 'stdout')):
            return run('ls postgresql-*').splitlines()[0]


def server(version=None):
    """
    Require a PostgreSQL server to be installed and running.

    ::

        from fabtools import require

        require.postgres.server()

    """
    if version:
        pkg_name = 'postgresql-%s' % version
    else:
        pkg_name = 'postgresql'
    package(pkg_name)

    started(_service_name(version))


def user(name, password):
    """
    Require a PostgreSQL user.

    ::

        from fabtools import require

        require.postgres.user('dbuser', password='somerandomstring')

    """
    if not user_exists(name):
        create_user(name, password)


def database(name, owner, template='template0', encoding='UTF8',
             locale='en_US.UTF-8'):
    """
    Require a PostgreSQL database.

    ::

        from fabtools import require

        require.postgres.database('myapp', owner='dbuser')

    """
    if not database_exists(name):

        with watch('/etc/locale.gen') as locales:
            require_locale(locale)
        if locales.changed:
            restarted(_service_name())

        create_database(name, owner, template=template, encoding=encoding,
            locale=locale)
