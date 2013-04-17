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

    from fabric.api import cd, run, sudo

    from fabtools import require
    from fabtools.files import (
        group,
        is_dir,
        md5sum,
        owner,
    )
    from fabtools.system import distrib_family

    from fabtools.require.git import working_copy

    family = distrib_family()
    if family == 'debian':
        require.deb.package('git-core')
    elif family == 'redhat':
        require.rpm.package('git')

    with cd('/tmp'):

        # Clean up
        sudo('rm -rf *')

        # Test with remote URL only
        working_copy(REMOTE_URL)
        assert is_dir('fabtools')
        assert is_dir('fabtools/.git')
        with cd('fabtools'):
            remotes = run('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'
            branch = run('git branch')
            assert branch == '* master'

        # Test with remote URL and path
        working_copy(REMOTE_URL, path='wc')
        assert is_dir('wc')
        assert is_dir('wc/.git')
        with cd('wc'):
            remotes = run('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'
            branch = run('git branch')
            assert branch == '* master'

        # Test that nothing is updated
        run('tar -c -f wc_old.tar --exclude .git wc')
        old_md5 = md5sum('wc_old.tar')
        working_copy(REMOTE_URL, path='wc', update=False)
        run('tar -c -f wc_new.tar --exclude .git wc')
        new_md5 = md5sum('wc_new.tar')
        assert old_md5 == new_md5

        # Test checkout of a branch
        working_copy(REMOTE_URL, path='wc', branch='test_git')
        assert is_dir('wc')
        assert is_dir('wc/.git')
        with cd('wc'):
            remotes = run('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'
            branch = run('git branch')
            assert branch == 'master\r\n* test_git'

        # Test use_sudo without user
        working_copy(REMOTE_URL, path='wc_root', use_sudo=True)
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

        # Test use_sudo with user nobody
        working_copy(REMOTE_URL, path='wc_nobody', use_sudo=True,
                     user='nobody')
        assert is_dir('wc_nobody')
        assert is_dir('wc_nobody/.git')
        with cd('wc_nobody'):
            remotes = sudo('git remote -v', user='nobody')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'
            branch = sudo('git branch', user='nobody')
            assert branch == '* master'
        assert owner('wc_nobody') == 'nobody'
        if family == 'debian':
            assert group('wc_nobody') == 'nogroup'
        elif family == 'redhat':
            assert group('wc_nobody') == 'nobody'
