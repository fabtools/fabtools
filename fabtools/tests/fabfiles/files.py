from __future__ import with_statement

import os
from pipes import quote
from tempfile import mkstemp
from functools import partial

from fabric.api import cd, env, run, sudo, task

from fabtools.utils import run_as_root


@task
def files():
    """
    Check file creation
    """

    from fabtools import require
    import fabtools

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

    from fabtools import require
    import fabtools

    with cd('/tmp'):

        run_as_root('rm -rf dir1 dir2')

        # Test directory creation

        require.directory('dir1')
        assert fabtools.files.is_dir('dir1')
        assert fabtools.files.owner('dir1') == env.user

        # Test initial owner requirement

        require.user('dirtest', create_home=False)
        require.directory('dir2', owner='dirtest', use_sudo=True)

        assert fabtools.files.is_dir('dir2')
        assert fabtools.files.owner('dir2') == 'dirtest'

        # Test changed owner requirement

        require.user('dirtest2', create_home=False)
        require.directory('dir2', owner='dirtest2', use_sudo=True)

        assert fabtools.files.is_dir('dir2')
        assert fabtools.files.owner('dir2') == 'dirtest2'


@task
def temporary_directories():
    """
    Check temporary directories
    """
    from fabtools.files import is_dir
    from fabtools.require.files import temporary_directory

    path1 = temporary_directory()
    path2 = temporary_directory()

    assert is_dir(path1)
    assert is_dir(path2)
    assert path1 != path2

    run('rmdir %s' % quote(path1))
    run('rmdir %s' % quote(path2))


@task
def temporary_directory_as_context_manager():
    """
    Check temporary directory used as a context manager
    """
    from fabtools.files import is_dir
    from fabtools.require.files import temporary_directory

    with temporary_directory() as path:
        assert is_dir(path)

        with cd(path):
            run('touch foo')

    assert not is_dir(path)


@task
def require_directory_has_correct_permissions():

    from fabtools.files import owner, group, mode
    from fabtools.require.files import directory as require_directory

    try:
        sudo('mkdir foo')
        require_directory('bar', use_sudo=True)

        assert owner('foo') == owner('bar')
        assert group('foo') == group('bar')
        assert mode('foo') == mode('bar')

    finally:
        sudo('rmdir foo bar')


@task
def require_empty_file_has_correct_permissions():

    from fabtools.files import owner, group, mode
    from fabtools.require.files import file as require_file

    try:
        sudo('touch foo')
        require_file('bar', use_sudo=True)

        assert owner('foo') == owner('bar')
        assert group('foo') == group('bar')
        assert mode('foo') == mode('bar')

    finally:
        sudo('rm -f foo bar')


@task
def require_file_with_contents_has_correct_permissions():

    from fabtools.files import owner, group, mode
    from fabtools.require.files import file as require_file

    try:
        sudo('echo "something" > foo')
        require_file('bar', contents='something', use_sudo=True)

        assert owner('foo') == owner('bar')
        assert group('foo') == group('bar')
        assert mode('foo') == mode('bar')

    finally:
        sudo('rm -f foo bar')


@task
def require_file_changes_ownership():

    from fabtools.files import owner
    from fabtools.require.files import file as require_file

    try:
        run('touch foo')
        assert owner('foo') == env.user

        require_file('foo', use_sudo=True)
        assert owner('foo') == 'root'

    finally:
        sudo('rm -f foo')
