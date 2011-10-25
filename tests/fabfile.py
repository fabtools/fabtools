import os
from tempfile import NamedTemporaryFile

from fabric.api import *
from fabtools import icanhaz
import fabtools


def files():
    """
    Check file creation
    """
    with cd('/tmp'):
        # Require that a file exists
        icanhaz.file('foo')
        assert fabtools.files.is_file('foo')
        assert run('cat foo') == '', run('cat foo')

        # Require that a file exists, whose contents should come from a URL
        icanhaz.file(url='http://www.google.com/robots.txt')
        assert fabtools.files.is_file('robots.txt')

        # Require that a file exists, whose contents should be this string
        bar_contents = '''This is the contents of the bar file'''
        icanhaz.file('bar', contents=bar_contents)
        assert fabtools.files.is_file('bar')
        assert run('cat bar') == bar_contents, run('cat bar')

        # Require that a file exists, whose contents should be this local file
        baz_contents = '''This is the contents of the bar file'''
        tmp_file = NamedTemporaryFile(delete=False)
        tmp_file.write(baz_contents)
        tmp_file.close()
        icanhaz.file('baz', source=tmp_file.name)
        os.remove(tmp_file.name)
        assert fabtools.files.is_file('baz')
        assert run('cat baz') == baz_contents, run('cat baz')


def mysql():
    """
    Setup MySQL server, user and database
    """
    icanhaz.mysql.server(password='s3cr3t')

    with settings(mysql_user='root', mysql_password='s3cr3t'):

        icanhaz.mysql.user('myuser', 'foo')
        assert fabtools.mysql.user_exists('myuser')

        icanhaz.mysql.database('mydb', owner='myuser')
        assert fabtools.mysql.database_exists('mydb')


def postgresql():
    """
    Setup PostgreSQL server, user and database
    """
    icanhaz.postgres.server()

    icanhaz.postgres.user('pguser', 'foo')
    assert fabtools.postgres.user_exists('pguser')

    icanhaz.postgres.database('pgdb', 'pguser')
    assert fabtools.postgres.database_exists('pgdb')
