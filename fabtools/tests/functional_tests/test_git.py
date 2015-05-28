# coding: utf-8
"""
Test high level git tools.  These tests should also cover the low
level tools as all of them are called indirectly.
"""

import functools

import pytest

from fabric.api import cd, run, sudo

from fabtools.files import group, is_dir, md5sum, owner
from fabtools.utils import run_as_root


pytestmark = pytest.mark.network


REMOTE_URL = 'https://github.com/disko/fabtools.git'


def test_git_require_remote_url():
    """
    Test with remote URL only
    """

    from fabtools.require.git import working_copy

    try:
        working_copy(REMOTE_URL)

        assert is_dir('fabtools')
        assert is_dir('fabtools/.git')

        with cd('fabtools'):
            remotes = run('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'

            assert _current_branch() == 'master'

    finally:
        run('rm -rf fabtools')


def test_git_require_remote_url_and_path():
    """
    Test working_copy() with remote URL and path
    """

    from fabtools.require.git import working_copy

    try:
        working_copy(REMOTE_URL, path='wc')

        assert is_dir('wc')
        assert is_dir('wc/.git')

        with cd('wc'):
            remotes = run('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'

            assert _current_branch() == 'master'

    finally:
        run('rm -rf wc')


def test_git_require_no_update():
    """
    Test working_copy() with update=False
    """

    from fabtools.require.git import working_copy

    try:
        working_copy(REMOTE_URL, path='wc')

        run('tar -c -f wc_old.tar --exclude .git wc')
        old_md5 = md5sum('wc_old.tar')

        working_copy(REMOTE_URL, path='wc', update=False)

        # Test that the working tree was not updated
        run('tar -c -f wc_new.tar --exclude .git wc')
        new_md5 = md5sum('wc_new.tar')
        assert old_md5 == new_md5

    finally:
        run('rm -rf wc')


def test_git_require_branch():
    """
    Test checkout of a branch
    """

    from fabtools.require.git import working_copy

    try:
        working_copy(REMOTE_URL, path='wc', branch='test_git')

        assert is_dir('wc')
        assert is_dir('wc/.git')

        with cd('wc'):
            remotes = run('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'

            assert _current_branch() == 'test_git'


    finally:
        run('rm -rf wc')


def test_git_require_sudo():
    """
    Test working_copy() with sudo
    """

    from fabtools.require.git import working_copy

    try:
        working_copy(REMOTE_URL, path='wc_root', use_sudo=True)

        assert is_dir('wc_root')
        assert is_dir('wc_root/.git')

        with cd('wc_root'):
            remotes = run('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'

            assert _current_branch() == 'master'

        assert owner('wc_root') == 'root'
        assert group('wc_root') == 'root'

    finally:
        run_as_root('rm -rf wc_root')


@pytest.yield_fixture(scope='module')
def gituser():
    from fabtools.require import user

    username = 'gituser'
    groupname = 'gitgroup'

    user(username, group=groupname)

    yield username, groupname

    run_as_root('userdel -r %s' % username)


def test_git_require_sudo_user(gituser):
    """
    Test working_copy() with sudo as a user
    """

    from fabtools.require.git import working_copy

    username, groupname = gituser

    with cd('/tmp'):
        try:
            working_copy(REMOTE_URL, path='wc_nobody', use_sudo=True, user=username)

            assert is_dir('wc_nobody')
            assert is_dir('wc_nobody/.git')

            with cd('wc_nobody'):
                remotes = sudo('git remote -v', user=username)
                assert remotes == \
                    'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                    'origin\thttps://github.com/disko/fabtools.git (push)'

                assert _current_branch() == 'master'

            assert owner('wc_nobody') == username
            assert group('wc_nobody') == groupname

        finally:
            run_as_root('rm -rf wc_nobody')


def _current_branch():
    return run('git rev-parse --abbrev-ref HEAD').stdout
