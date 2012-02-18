import hashlib
import mock
import unittest


class FilesTestCase(unittest.TestCase):

    def _file(self, *args, **kwargs):
        """ Proxy to ensure ImportErrors actually cause test failures rather
        than trashing the test run entirely """
        from fabtools import require
        require.files.file(*args, **kwargs)

    @mock.patch('fabtools.require.files.md5sum')
    @mock.patch('fabtools.require.files.is_file')
    def test_verify_remote_false(self, is_file, md5sum):
        """ If verify_remote is set to False, then we should find that
        only is_file is used to check for the file's existence. Hashlib's
        md5 should not have been called.
        """
        is_file.return_value = True
        self._file(contents='This is a test', verify_remote=False)
        self.assertTrue(is_file.called)
        self.assertFalse(md5sum.called)

    @mock.patch('fabtools.require.files.md5sum')
    @mock.patch('fabtools.require.files.is_file')
    def test_verify_remote_true(self, is_file, md5sum):
        """ If verify_remote is True, then we should find that an MD5 hash is
        used to work out whether the file is different.
        """
        is_file.return_value = True
        md5sum.return_value = hashlib.md5('This is a test').hexdigest()
        self._file(contents='This is a test', verify_remote=True)
        self.assertTrue(is_file.called)
        self.assertTrue(md5sum.called)


class PostgresTestCase(unittest.TestCase):

    @mock.patch('fabtools.require.postgres.create_database')
    @mock.patch('fabtools.require.postgres.database_exists')
    def test_params_respected(self, database_exists, create_database):
        """ If require.database is called, ensure that the template, encoding
        and locale parameters are passed through to the underlying
        create_database call """
        from fabtools import require
        database_exists.return_value = False
        require.postgres.database('foo', 'bar', locale='some_locale',
            encoding='some_encoding', template='some_template')
        create_database.assert_called_with('foo', 'bar', locale='some_locale',
            encoding='some_encoding', template='some_template')
