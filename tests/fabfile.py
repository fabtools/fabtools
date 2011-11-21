import os
from tempfile import NamedTemporaryFile

from fabric.api import *
from fabtools import require
import fabtools


def files():
    """
    Check file creation
    """
    with cd('/tmp'):
        # Require that a file exists
        require.file('foo')
        assert fabtools.files.is_file('foo')
        assert run('cat foo') == '', run('cat foo')

        # Require that a file exists, whose contents should come from a URL
        require.file(url='http://www.google.com/robots.txt')
        assert fabtools.files.is_file('robots.txt')

        # Require that a file exists, whose contents should be this string
        bar_contents = '''This is the contents of the bar file'''
        require.file('bar', contents=bar_contents)
        assert fabtools.files.is_file('bar')
        assert run('cat bar') == bar_contents, run('cat bar')

        # Require that a file exists, whose contents should be this local file
        baz_contents = '''This is the contents of the bar file'''
        tmp_file = NamedTemporaryFile(delete=False)
        tmp_file.write(baz_contents)
        tmp_file.close()
        require.file('baz', source=tmp_file.name)
        os.remove(tmp_file.name)
        assert fabtools.files.is_file('baz')
        assert run('cat baz') == baz_contents, run('cat baz')


def python():
    """
    Check Python package installation
    """
    require.python.virtualenv('/tmp/venv', python='python2.6')
    assert fabtools.files.is_dir('/tmp/venv')
    assert fabtools.files.is_file('/tmp/venv/bin/python')

    require.python.package('fabric', virtualenv='/tmp/venv')
    assert fabtools.files.is_dir('/tmp/venv/lib/python2.6/site-packages/fabric')


def mysql():
    """
    Setup MySQL server, user and database
    """
    require.mysql.server(password='s3cr3t')

    with settings(mysql_user='root', mysql_password='s3cr3t'):

        require.mysql.user('myuser', 'foo')
        assert fabtools.mysql.user_exists('myuser')

        require.mysql.database('mydb', owner='myuser')
        assert fabtools.mysql.database_exists('mydb')


def postgresql():
    """
    Setup PostgreSQL server, user and database
    """
    require.postgres.server()

    require.postgres.user('pguser', 'foo')
    assert fabtools.postgres.user_exists('pguser')

    require.postgres.database('pgdb', 'pguser')
    assert fabtools.postgres.database_exists('pgdb')
