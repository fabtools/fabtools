# coding: utf-8
"""
Test high level git tools.  These tests should also cover the low
level tools as all of them are called indirectly.
"""

from __future__ import with_statement

from fabric.api import cd, run, sudo

from fabtools import require
from fabtools.files import group, is_dir, md5sum, owner
from fabtools.tests.vagrant_test_case import VagrantTestCase
from fabtools.utils import run_as_root


REMOTE_URL = 'https://github.com/disko/fabtools.git'


class TestGitWorkingCopy(VagrantTestCase):

    def test_git_require_remote_url(self):
        """
        Test with remote URL only
        """

        require.git.working_copy(REMOTE_URL)

        self.assertTrue(is_dir('fabtools'))
        self.assertTrue(is_dir('fabtools/.git'))

        with cd('fabtools'):
            remotes = run('git remote -v')
            self.assertEqual(remotes,
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)')

            branch = run('git branch')
            self.assertEqual(branch, '* master')

        run('rm -rf fabtools')

    def test_git_require_remote_url_and_path(self):
        """
        Test working_copy() with remote URL and path
        """

        require.git.working_copy(REMOTE_URL, path='wc')

        self.assertTrue(is_dir('wc'))
        self.assertTrue(is_dir('wc/.git'))

        with cd('wc'):
            remotes = run('git remote -v')
            self.assertEqual(remotes,
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)')

            branch = run('git branch')
            self.assertEqual(branch, '* master')

        run('rm -rf wc')

    def test_git_require_no_update(self):
        """
        Test working_copy() with update=False
        """

        require.git.working_copy(REMOTE_URL, path='wc')

        run('tar -c -f wc_old.tar --exclude .git wc')
        old_md5 = md5sum('wc_old.tar')

        require.git.working_copy(REMOTE_URL, path='wc', update=False)

        # Test that the working tree was not updated
        run('tar -c -f wc_new.tar --exclude .git wc')
        new_md5 = md5sum('wc_new.tar')
        self.assertEqual(old_md5, new_md5)

    def test_git_require_branch(self):
        """
        Test checkout of a branch
        """

        require.git.working_copy(REMOTE_URL, path='wc', branch='test_git')

        self.assertTrue(is_dir('wc'))
        self.assertTrue(is_dir('wc/.git'))

        with cd('wc'):
            remotes = run('git remote -v')
            self.assertEqual(remotes,
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)')

            branch = run('git branch')
            self.assertEqual(branch, 'master\r\n* test_git')

        run('rm -rf wc')

    def test_git_require_sudo(self):
        """
        Test working_copy() with sudo
        """

        require.git.working_copy(REMOTE_URL, path='wc_root', use_sudo=True)

        self.assertTrue(is_dir('wc_root'))
        self.assertTrue(is_dir('wc_root/.git'))

        with cd('wc_root'):
            remotes = run('git remote -v')
            self.assertEqual(remotes,
                'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                'origin\thttps://github.com/disko/fabtools.git (push)')

            branch = run('git branch')
            self.assertEqual(branch, '* master')

        self.assertEqual(owner('wc_root'), 'root')
        self.assertEqual(group('wc_root'), 'root')

        run_as_root('rm -rf wc_root')

    def test_git_require_sudo_user(self):
        """
        Test working_copy() with sudo as a user
        """

        require.user('gituser', group='gitgroup')

        with cd('/tmp'):
            require.git.working_copy(REMOTE_URL, path='wc_nobody', use_sudo=True,
                                     user='gituser')

            self.assertTrue(is_dir('wc_nobody'))
            self.assertTrue(is_dir('wc_nobody/.git'))

            with cd('wc_nobody'):
                remotes = sudo('git remote -v', user='gituser')
                self.assertEqual(remotes,
                    'origin\thttps://github.com/disko/fabtools.git (fetch)\r\n' \
                    'origin\thttps://github.com/disko/fabtools.git (push)')

                branch = sudo('git branch', user='gituser')
                self.assertEqual(branch, '* master')

            self.assertEqual(owner('wc_nobody'), 'gituser')
            self.assertEqual(group('wc_nobody'), 'gitgroup')

            run_as_root('rm -rf wc_nobody')

        run_as_root('userdel gituser')
        run_as_root('groupdel gitgroup')
