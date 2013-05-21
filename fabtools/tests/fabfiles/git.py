# coding: utf-8

from __future__ import with_statement

from fabric.api import task


REMOTE_URL = 'https://github.com/disko/fabtools.git'


@task
def git_require():
    """
    Test high level git tools.  These tests should also cover the low
    level tools as all of them are called indirectly.
    """

    from fabric.api import cd, sudo

    with cd('/tmp'):

        # Clean up
        sudo('rm -rf *')

        git_require_remote_url()
        git_require_remote_url_and_path()
        git_require_no_update()
        git_require_branch()
        git_require_sudo()
        git_require_sudo_user()


def git_require_remote_url():
    """
    Test with remote URL only
    """

    from fabric.api import cd, run

    from fabtools.files import is_dir
    from fabtools import require

    require.git.working_copy(REMOTE_URL)

    assert is_dir('fabtools')
    assert is_dir('fabtools/.git')
    with cd('fabtools'):
        remotes = run('git remote -v')
        assert remotes == \
            'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
            'origin\thttps://github.com/disko/fabtools.git (push)'
        branch = run('git branch')
        assert branch == '* master'


def git_require_remote_url_and_path():
    """
    Test working_copy() with remote URL and path
    """

    from fabric.api import cd, run

    from fabtools.files import is_dir
    from fabtools import require

    require.git.working_copy(REMOTE_URL, path='wc')

    assert is_dir('wc')
    assert is_dir('wc/.git')
    with cd('wc'):
        remotes = run('git remote -v')
        assert remotes == \
            'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
            'origin\thttps://github.com/disko/fabtools.git (push)'
        branch = run('git branch')
        assert branch == '* master'


def git_require_no_update():
    """
    Test working_copy() with update=False
    """
    from fabric.api import run

    from fabtools.files import md5sum
    from fabtools import require

    run('tar -c -f wc_old.tar --exclude .git wc')
    old_md5 = md5sum('wc_old.tar')

    require.git.working_copy(REMOTE_URL, path='wc', update=False)

    # Test that the working tree was not updated
    run('tar -c -f wc_new.tar --exclude .git wc')
    new_md5 = md5sum('wc_new.tar')
    assert old_md5 == new_md5


def git_require_branch():
    """
    Test checkout of a branch
    """

    from fabric.api import cd, run

    from fabtools.files import is_dir
    from fabtools import require

    require.git.working_copy(REMOTE_URL, path='wc', branch='test_git')

    assert is_dir('wc')
    assert is_dir('wc/.git')
    with cd('wc'):
        remotes = run('git remote -v')
        assert remotes == \
            'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
            'origin\thttps://github.com/disko/fabtools.git (push)'
        branch = run('git branch')
        assert branch == 'master\r\n* test_git'


def git_require_sudo():
    """
    Test working_copy() with sudo
    """

    from fabric.api import cd, sudo

    from fabtools.files import group, is_dir, owner
    from fabtools import require

    require.git.working_copy(REMOTE_URL, path='wc_root', use_sudo=True)

    assert is_dir('wc_root')
    assert is_dir('wc_root/.git')
    with cd('wc_root'):
        remotes = sudo('git remote -v')
        assert remotes == \
            'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
            'origin\thttps://github.com/disko/fabtools.git (push)'
        branch = sudo('git branch')
        assert branch == '* master'
    assert owner('wc_root') == 'root'
    assert group('wc_root') == 'root'


def git_require_sudo_user():
    """
    Test working_copy() with sudo as a user
    """

    from fabric.api import cd, sudo

    from fabtools.files import group, is_dir, owner
    from fabtools import require

    require.user('gituser', group='gitgroup')

    require.git.working_copy(REMOTE_URL, path='wc_nobody', use_sudo=True,
                             user='gituser')

    assert is_dir('wc_nobody')
    assert is_dir('wc_nobody/.git')
    with cd('wc_nobody'):
        remotes = sudo('git remote -v', user='gituser')
        assert remotes == \
            'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
            'origin\thttps://github.com/disko/fabtools.git (push)'
        branch = sudo('git branch', user='gituser')
        assert branch == '* master'
    assert owner('wc_nobody') == 'gituser'
    assert group('wc_nobody') == 'gitgroup'
