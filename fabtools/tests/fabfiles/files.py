from __future__ import with_statement

import os
from tempfile import mkstemp
from functools import partial

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

        # Ensure that changes to watched file are detected
        require.file('watched', contents='aaa')
        with fabtools.files.watch('watched') as f:
            require.file('watched', contents='bbb')
        assert f.changed
        with fabtools.files.watch('watched') as f:
            pass
        assert not f.changed

        # Ensure that the callable is triggered only
        # when the watched file is modified
        require.file('watched', contents='aaa')
        with fabtools.files.watch('watched', callback=partial(require.file, 'modified1')):
            require.file('watched', contents='bbb')
        assert fabtools.files.is_file('modified1')
        with fabtools.files.watch('watched', callback=partial(require.file, 'modified2')):
            pass
        assert not fabtools.files.is_file('modified2')


@task
def directories():
    """
    Check directory creation and modification
    """

    with cd('/tmp'):

        sudo('rm -rf dir1 dir2')

        # Test directory creation

        require.directory('dir1')
        assert fabtools.files.is_dir('dir1')
        assert fabtools.files.owner('dir1') == env.user

        # Test initial owner requirement

        require.user('dirtest')
        require.directory('dir2', owner='dirtest', use_sudo=True)

        assert fabtools.files.is_dir('dir2')
        assert fabtools.files.owner('dir2') == 'dirtest'

        # Test changed owner requirement

        require.user('dirtest2')
        require.directory('dir2', owner='dirtest2', use_sudo=True)

        assert fabtools.files.is_dir('dir2')
        assert fabtools.files.owner('dir2') == 'dirtest2'
