import hashlib
import unittest

from mock import patch
import pytest


@patch('fabtools.require.files._mode')
@patch('fabtools.require.files._owner')
@patch('fabtools.require.files.umask')
@patch('fabtools.require.files.put')
@patch('fabtools.require.files.md5sum')
@patch('fabtools.require.files.is_file')
class FilesTestCase(unittest.TestCase):

    def _file(self, *args, **kwargs):
        """ Proxy to ensure ImportErrors actually cause test failures rather
        than trashing the test run entirely """
        from fabtools import require
        require.files.file(*args, **kwargs)

    def test_verify_remote_false(self, is_file, md5sum, put, umask, owner, mode):
        """ If verify_remote is set to False, then we should find that
        only is_file is used to check for the file's existence. Hashlib's
        md5 should not have been called.
        """
        is_file.return_value = True
        self._file(contents='This is a test', verify_remote=False)
        self.assertTrue(is_file.called)
        self.assertFalse(md5sum.called)

    def test_verify_remote_true(self, is_file, md5sum, put, umask, owner, mode):
        """ If verify_remote is True, then we should find that an MD5 hash is
        used to work out whether the file is different.
        """
        is_file.return_value = True
        md5sum.return_value = hashlib.md5('This is a test').hexdigest()
        self._file(contents='This is a test', verify_remote=True)
        self.assertTrue(is_file.called)
        self.assertTrue(md5sum.called)

    def test_temp_dir(self, is_file, md5sum, put, umask, owner, mode):
        owner.return_value = 'root'
        umask.return_value = '0002'
        mode.return_value = '0664'
        from fabtools import require
        require.file('/var/tmp/foo', source=__file__, use_sudo=True, temp_dir='/somewhere')
        put.assert_called_with(__file__, '/var/tmp/foo', use_sudo=True, temp_dir='/somewhere')

    def test_home_as_temp_dir(self, is_file, md5sum, put, umask, owner, mode):
        owner.return_value = 'root'
        umask.return_value = '0002'
        mode.return_value = '0664'
        from fabtools import require
        require.file('/var/tmp/foo', source=__file__, use_sudo=True, temp_dir='')
        put.assert_called_with(__file__, '/var/tmp/foo', use_sudo=True, temp_dir='')

    def test_default_temp_dir(self, is_file, md5sum, put, umask, owner, mode):
        owner.return_value = 'root'
        umask.return_value = '0002'
        mode.return_value = '0664'
        from fabtools import require
        require.file('/var/tmp/foo', source=__file__, use_sudo=True)
        put.assert_called_with(__file__, '/var/tmp/foo', use_sudo=True, temp_dir='/tmp')


class TestUploadTemplate(unittest.TestCase):

    @patch('fabtools.files.run')
    @patch('fabtools.files._upload_template')
    def test_mkdir(self, mock_upload_template, mock_run):

        from fabtools.files import upload_template

        upload_template('filename', '/path/to/destination', mkdir=True)

        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], 'mkdir -p /path/to')

    @patch('fabtools.files.sudo')
    @patch('fabtools.files._upload_template')
    def test_mkdir_sudo(self, mock_upload_template, mock_sudo):

        from fabtools.files import upload_template

        upload_template('filename', '/path/to/destination', mkdir=True, use_sudo=True)

        args, kwargs = mock_sudo.call_args
        self.assertEqual(args[0], 'mkdir -p /path/to')
        self.assertEqual(kwargs['user'], None)

    @patch('fabtools.files.sudo')
    @patch('fabtools.files._upload_template')
    def test_mkdir_sudo_user(self, mock_upload_template, mock_sudo):

        from fabtools.files import upload_template

        upload_template('filename', '/path/to/destination', mkdir=True, use_sudo=True, user='alice')

        args, kwargs = mock_sudo.call_args
        self.assertEqual(args[0], 'mkdir -p /path/to')
        self.assertEqual(kwargs['user'], 'alice')

    @patch('fabtools.files.run_as_root')
    @patch('fabtools.files._upload_template')
    def test_chown(self, mock_upload_template, mock_run_as_root):

        from fabric.api import env
        from fabtools.files import upload_template

        upload_template('filename', 'destination', chown=True)

        args, kwargs = mock_run_as_root.call_args
        self.assertEqual(args[0], 'chown %s: destination' % env.user)

    @patch('fabtools.files.run_as_root')
    @patch('fabtools.files._upload_template')
    def test_chown_user(self, mock_upload_template, mock_run_as_root):

        from fabtools.files import upload_template

        upload_template('filename', 'destination', chown=True, user='alice')

        args, kwargs = mock_run_as_root.call_args
        self.assertEqual(args[0], 'chown alice: destination')

    @patch('fabtools.files._upload_template')
    def test_use_jinja_true(self, mock_upload_template):

        from fabtools.files import upload_template

        upload_template('filename', 'destination', use_jinja=True)

        args, kwargs = mock_upload_template.call_args
        self.assertEqual(kwargs['use_jinja'], True)

    @patch('fabtools.files._upload_template')
    def test_use_jinja_false(self, mock_upload_template):

        from fabtools.files import upload_template

        upload_template('filename', 'destination', use_jinja=False)

        args, kwargs = mock_upload_template.call_args
        self.assertEqual(kwargs['use_jinja'], False)


@pytest.yield_fixture(scope='module')
def mock_run():
    with patch('fabtools.files.run') as mock:
        yield mock


def test_copy(mock_run):
    from fabtools.files import copy
    copy('/tmp/src', '/tmp/dst')
    mock_run.assert_called_with('/bin/cp /tmp/src /tmp/dst')


def test_copy_recursive(mock_run):
    from fabtools.files import copy
    copy('/tmp/src', '/tmp/dst', recursive=True)
    mock_run.assert_called_with('/bin/cp -r /tmp/src /tmp/dst')


def test_move(mock_run):
    from fabtools.files import move
    move('/tmp/src', '/tmp/dst')
    mock_run.assert_called_with('/bin/mv /tmp/src /tmp/dst')


def test_symlink(mock_run):
    from fabtools.files import symlink
    symlink('/tmp/src', '/tmp/dst')
    mock_run.assert_called_with('/bin/ln -s /tmp/src /tmp/dst')


def test_remove(mock_run):
    from fabtools.files import remove
    remove('/tmp/src')
    mock_run.assert_called_with('/bin/rm /tmp/src')


def test_remove_recursive(mock_run):
    from fabtools.files import remove
    remove('/tmp/src', recursive=True)
    mock_run.assert_called_with('/bin/rm -r /tmp/src')
