# -*- coding: utf-8 -*-

"""
Created on 2013-03-04
:author: Andreas Kaiser (disko)
"""

from __future__ import with_statement

from fabric.api import cd
from fabric.api import sudo
from fabric.api import task

from fabtools import require
from fabtools.files import group
from fabtools.files import is_dir
from fabtools.files import owner


remote_url = "https://github.com/disko/fabtools.git"


@task
def git_require():
    """ Test high level git tools.  These tests should also cover the low level
        tools as all of them are called indirectly. """

    require.deb.package('git')

    from fabtools.require.git import working_copy

    with cd('/tmp'):
        # clean up...
        sudo('rm -rf *')

        # working_copy(remote_url, path=None, branch="master", update=True,
        #              use_sudo=False, user=None)

        # Test with remote_url only
        working_copy(remote_url)
        assert is_dir('fabtools')
        assert is_dir('fabtools/.git')
        with cd('fabtools'):
            remotes = sudo('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'
            branch = sudo('git branch')
            assert branch == '* master'

        # Test with remote_url and path
        working_copy(remote_url, path='wc')
        assert is_dir('wc')
        assert is_dir('wc/.git')
        with cd('wc'):
            remotes = sudo('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'
            branch = sudo('git branch')
            assert branch == '* master'

        # Test that nothing is upated
        sudo('tar cf wc_old.tar wc')
        old_md5 = sudo('md5sum wc_old.tar').split(' ')[0]
        working_copy(remote_url, path='wc', update=False)
        sudo('tar cf wc_new.tar wc')
        new_md5 = sudo('md5sum wc_new.tar').split(' ')[0]
        assert old_md5 == new_md5

        # Test checkout of a branch
        working_copy(remote_url, path='wc', branch="test_git")
        assert is_dir('wc')
        assert is_dir('wc/.git')
        with cd('wc'):
            remotes = sudo('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'
            branch = sudo('git branch')
            assert branch == 'master\r\n* test_git'

        # Test use_sudo without user
        working_copy(remote_url, path='wc_root', use_sudo=True)
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
        working_copy(remote_url, path='wc_nobody', use_sudo=True,
                     user='nobody')
        assert is_dir('wc_nobody')
        assert is_dir('wc_nobody/.git')
        with cd('wc_nobody'):
            remotes = sudo('git remote -v')
            assert remotes == \
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)'
            branch = sudo('git branch')
            assert branch == '* master'
        assert owner('wc_nobody') == 'nobody'
        assert group('wc_nobody') == 'nogroup'
