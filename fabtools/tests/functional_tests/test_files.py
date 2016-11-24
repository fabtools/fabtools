import os
from pipes import quote
from tempfile import mkstemp
from functools import partial

import pytest

from fabric.api import cd, env, run

from fabtools.files import is_dir, is_file, owner
from fabtools.utils import run_as_root


def test_require_file():
    """
    Require that a file exists, whose contents should come from a URL
    """
    from fabtools.require import file as require_file

    try:
        require_file('foo')

        assert is_file('foo')
        assert run('cat foo') == ''

    finally:
        run('rm -f foo')


@pytest.mark.network
def test_require_file_from_url():
    """
    Require that a file exists, whose contents should come from a URL
    """
    from fabtools.require import file as require_file

    try:
        require_file(url='http://www.google.com/robots.txt')

        assert is_file('robots.txt')

    finally:
        run('rm -f robots.txt')


def test_require_file_from_string():
    """
    Require that a file exists, whose contents should be this string
    """
    from fabtools.require import file as require_file

    try:
        bar_contents = "This is the contents of the bar file"

        require_file('bar', contents=bar_contents)

        assert is_file('bar')
        assert run('cat bar') == bar_contents

    finally:
        run('rm -f bar')


def test_require_file_from_local_file():
    """
    Require that a file exists, whose contents should be this local file
    """
    from fabtools.require import file as require_file

    try:
        baz_contents = "This is the contents of the bar file"
        fd, filename = mkstemp()
        tmp_file = os.fdopen(fd, 'w')
        tmp_file.write(baz_contents)
        tmp_file.close()

        require_file('baz', source=filename)

        assert is_file('baz')
        assert run('cat baz') == baz_contents

    finally:
        os.remove(filename)
        run('rm -f baz')


def test_empty_file_has_correct_permissions():

    from fabtools.files import owner, group, mode
    from fabtools.require.files import file as require_file

    try:
        run_as_root('touch foo')
        require_file('bar', use_sudo=True)

        assert owner('foo') == owner('bar')
        assert group('foo') == group('bar')
        assert mode('foo') == mode('bar')

    finally:
        run_as_root('rm -f foo bar')


def test_file_with_contents_has_correct_permissions():

    from fabtools.files import owner, group, mode
    from fabtools.require.files import file as require_file

    try:
        run_as_root('echo "something" > foo')
        require_file('bar', contents='something', use_sudo=True)

        assert owner('foo') == owner('bar')
        assert group('foo') == group('bar')
        assert mode('foo') == mode('bar')

    finally:
        run_as_root('rm -f foo bar')


def test_file_changes_ownership():

    from fabtools.files import owner
    from fabtools.require.files import file as require_file

    try:
        run('touch foo')
        assert owner('foo') == env.user

        require_file('foo', use_sudo=True)
        assert owner('foo') == 'root'

    finally:
        run_as_root('rm -f foo')


@pytest.fixture()
def watched_file():
    from fabtools.require import file as require_file
    filename= 'watched'
    require_file('watched', contents='aaa')
    return filename


def test_flag_is_set_when_watched_file_is_modified(watched_file):

    from fabtools.files import watch
    from fabtools.require import file as require_file

    with watch('watched') as f:
        require_file('watched', contents='bbb')

    assert f.changed


def test_flag_is_not_set_when_watched_file_is_not_modified(watched_file):

    from fabtools.files import watch

    with watch('watched') as f:
        pass

    assert not f.changed


def test_callback_is_called_when_watched_file_is_modified(watched_file):

    from fabtools.files import watch
    from fabtools.require import file as require_file

    try:
        with watch('watched', callback=partial(require_file, 'modified1')):
            require_file('watched', contents='bbb')

        assert is_file('modified1')

    finally:
        run('rm -f modified1')


def test_callback_is_not_called_when_watched_file_is_not_modified(watched_file):

    from fabtools.files import watch
    from fabtools.require import file as require_file

    try:
        with watch('watched', callback=partial(require_file, 'modified2')):
            pass

        assert not is_file('modified2')

    finally:
        run('rm -f modified2')


@pytest.yield_fixture(scope='module')
def users():

    from fabtools.require import user as require_user
    from fabtools.user import exists

    test_users = ['testuser', 'testuser2']

    for username in test_users:
        require_user(username, create_home=False)

    yield

    for username in test_users:
        if exists(username):
            run_as_root('userdel %s' % username)


def test_directory_creation():

    from fabtools.require import directory

    try:
        directory('testdir')

        assert is_dir('testdir')
        assert owner('testdir') == env.user

    finally:
        run('rmdir testdir')


def test_initial_owner_requirement(users):

    from fabtools.require import directory

    try:
        directory('testdir', owner='testuser', use_sudo=True)

        assert is_dir('testdir')
        assert owner('testdir') == 'testuser'

    finally:
        run_as_root('rmdir testdir')


def test_changed_owner_requirement(users):

    from fabtools.require import directory

    try:
        directory('testdir', owner='testuser', use_sudo=True)
        directory('testdir', owner='testuser2', use_sudo=True)

        assert is_dir('testdir')
        assert owner('testdir') == 'testuser2'

    finally:
        run_as_root('rmdir testdir')


def test_permissions():

    from fabtools.files import owner, group, mode
    from fabtools.require.files import directory as require_directory

    try:
        run_as_root('mkdir foo')
        require_directory('bar', use_sudo=True)

        assert owner('foo') == owner('bar')
        assert group('foo') == group('bar')
        assert mode('foo') == mode('bar')

    finally:
        run_as_root('rmdir foo bar')


def test_temporary_directory_as_function():

    from fabtools.files import is_dir
    from fabtools.require.files import temporary_directory

    path1 = temporary_directory()
    path2 = temporary_directory()

    assert is_dir(path1)
    assert is_dir(path2)
    assert path1 != path2

    run('rmdir %s' % quote(path1))
    run('rmdir %s' % quote(path2))


def test_temporary_directory_as_context_manager():

    from fabtools.files import is_dir
    from fabtools.require.files import temporary_directory

    with temporary_directory() as path:
        assert is_dir(path)

        with cd(path):
            run('touch foo')

    assert not is_dir(path)
