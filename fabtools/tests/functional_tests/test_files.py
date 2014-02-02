from __future__ import with_statement

import os
from pipes import quote
from tempfile import mkstemp
from functools import partial

from fabric.api import cd, env, run, sudo

from fabtools import require
from fabtools.utils import run_as_root
import fabtools

from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestRequireFile(VagrantTestCase):
    """
    Check file creation
    """

    @classmethod
    def setUpClass(cls):
        run('rm -f foo bar baz robots.txt')

    @classmethod
    def tearDownClass(cls):
        run('rm -f foo bar baz robots.txt')

    def test_require_file(self):
        """
        Require that a file exists, whose contents should come from a URL
        """
        require.file('foo')
        self.assertTrue(fabtools.files.is_file('foo'))
        self.assertEqual(run('cat foo'), '')

    def test_require_file_from_url(self):
        """
        Require that a file exists, whose contents should come from a URL
        """
        require.file(url='http://www.google.com/robots.txt')
        self.assertTrue(fabtools.files.is_file('robots.txt'))

    def test_require_file_from_string(self):
        """
        Require that a file exists, whose contents should be this string
        """
        bar_contents = '''This is the contents of the bar file'''
        require.file('bar', contents=bar_contents)
        self.assertTrue(fabtools.files.is_file('bar'))
        self.assertEqual(run('cat bar'), bar_contents)

    def test_require_file_from_local_file(self):
        """
        Require that a file exists, whose contents should be this local file
        """
        baz_contents = '''This is the contents of the bar file'''
        fd, filename = mkstemp()
        tmp_file = os.fdopen(fd, 'w')
        tmp_file.write(baz_contents)
        tmp_file.close()

        require.file('baz', source=filename)

        os.remove(filename)

        self.assertTrue(fabtools.files.is_file('baz'))
        self.assertEqual(run('cat baz'), baz_contents)

    def test_empty_file_has_correct_permissions(self):

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

    def test_file_with_contents_has_correct_permissions(self):

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

    def test_file_changes_ownership(self):

        from fabtools.files import owner
        from fabtools.require.files import file as require_file

        try:
            run('touch foo')
            assert owner('foo') == env.user

            require_file('foo', use_sudo=True)
            assert owner('foo') == 'root'

        finally:
            sudo('rm -f foo')


class TestWatch(VagrantTestCase):
    """
    Check behaviour of the watch context manager
    """

    @classmethod
    def setUpClass(cls):
        run('rm -f watch modified1 modified2', quiet=True)

    @classmethod
    def tearDownClass(cls):
        run('rm -f watched modified1 modified2', quiet=True)

    def setUp(self):
        require.file('watched', contents='aaa')

    def test_flag_is_set_when_watched_file_is_modified(self):
        with fabtools.files.watch('watched') as f:
            require.file('watched', contents='bbb')
        self.assertTrue(f.changed)

    def test_flag_is_not_set_when_watched_file_is_not_modified(self):
        with fabtools.files.watch('watched') as f:
            pass
        self.assertFalse(f.changed)

    def test_callback_is_called_when_watched_file_is_modified(self):
        with fabtools.files.watch('watched', callback=partial(require.file, 'modified1')):
            require.file('watched', contents='bbb')
        assert fabtools.files.is_file('modified1')

    def test_callback_is_not_called_when_watched_file_is_not_modified(self):
        with fabtools.files.watch('watched', callback=partial(require.file, 'modified2')):
            pass
        assert not fabtools.files.is_file('modified2')


class TestRequireDirectory(VagrantTestCase):
    """
    Check directory creation and modification
    """

    @classmethod
    def setUpClass(cls):
        require.user('testuser', create_home=False)
        require.user('testuser2', create_home=False)

    @classmethod
    def tearDownClass(cls):
        for user in ['testuser', 'testuser2']:
            if fabtools.user.exists(user):
                run_as_root('userdel %s' % user)

    def setUp(self):
        run_as_root('rm -rf testdir')

    def tearDown(self):
        run_as_root('rm -rf testdir')

    def test_directory_creation(self):
        require.directory('testdir')
        self.assertTrue(fabtools.files.is_dir('testdir'))
        self.assertEqual(fabtools.files.owner('testdir'), env.user)

    def test_initial_owner_requirement(self):
        require.directory('testdir', owner='testuser', use_sudo=True)
        self.assertTrue(fabtools.files.is_dir('testdir'))
        self.assertEqual(fabtools.files.owner('testdir'), 'testuser')

    def test_changed_owner_requirement(self):
        require.directory('testdir', owner='testuser', use_sudo=True)
        require.directory('testdir', owner='testuser2', use_sudo=True)
        self.assertTrue(fabtools.files.is_dir('testdir'))
        self.assertEqual(fabtools.files.owner('testdir'), 'testuser2')

    def test_permissions(self):

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


class TestTemporaryDirectory(VagrantTestCase):
    """
    Check temporary directories
    """

    def test_temporary_directory_as_function(self):

        from fabtools.files import is_dir
        from fabtools.require.files import temporary_directory

        path1 = temporary_directory()
        path2 = temporary_directory()

        assert is_dir(path1)
        assert is_dir(path2)
        assert path1 != path2

        run('rmdir %s' % quote(path1))
        run('rmdir %s' % quote(path2))

    def test_temporary_directory_as_context_manager(self):

        from fabtools.files import is_dir
        from fabtools.require.files import temporary_directory

        with temporary_directory() as path:
            assert is_dir(path)

            with cd(path):
                run('touch foo')

        assert not is_dir(path)
