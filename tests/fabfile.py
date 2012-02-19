from __future__ import with_statement

from tempfile import mkstemp
import hashlib
import os

from fabric.api import *
from fabtools import require
import fabtools


@task
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
        fd, filename = mkstemp()
        tmp_file = os.fdopen(fd, 'w')
        tmp_file.write(baz_contents)
        tmp_file.close()
        require.file('baz', source=filename)
        os.remove(filename)
        assert fabtools.files.is_file('baz')
        assert run('cat baz') == baz_contents, run('cat baz')

        # Ensure that the callable is triggered only
        # when the watched file is modified
        require.file('watched', contents='aaa')
        with fabtools.files.watch('watched', False, require.file, 'modified1'):
            require.file('watched', contents='bbb')
        assert fabtools.files.is_file('modified1')
        with fabtools.files.watch('watched', False, require.file, 'modified2'):
            pass
        assert not fabtools.files.is_file('modified2')


@task
def md5():
    """
    Check MD5 sums (unavailable, empty, with content)
    """
    with cd('/tmp'):
        run('touch f1')
        run('echo -n hello > f2')
        assert fabtools.files.md5sum('doesnotexist') is None
        assert fabtools.files.md5sum('f1') == hashlib.md5('').hexdigest()
        assert fabtools.files.md5sum('f2') == hashlib.md5('hello').hexdigest()


@task
def python():
    """
    Check Python package installation
    """
    require.python.virtualenv('/tmp/venv')
    assert fabtools.files.is_dir('/tmp/venv')
    assert fabtools.files.is_file('/tmp/venv/bin/python')

    with fabtools.python.virtualenv('/tmp/venv'):
        require.python.package('fabric')
    assert fabtools.files.is_file('/tmp/venv/bin/fab')


@task
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


@task
def postgresql():
    """
    Setup PostgreSQL server, user and database
    """
    require.postgres.server()

    require.postgres.user('pguser', 'foo')
    assert fabtools.postgres.user_exists('pguser')

    require.postgres.database('pgdb', 'pguser')
    assert fabtools.postgres.database_exists('pgdb')
