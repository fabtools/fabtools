import mock
import unittest


class PostgresTestCase(unittest.TestCase):

    @mock.patch('fabtools.require.postgres._service_name')
    @mock.patch('fabtools.require.postgres.restarted')
    @mock.patch('fabtools.require.postgres.watch')
    @mock.patch('fabtools.require.postgres.require_locale')
    @mock.patch('fabtools.require.postgres.create_database')
    @mock.patch('fabtools.require.postgres.database_exists')
    def test_params_respected(self, database_exists, create_database,
        require_locale, watch, restarted, service_name):
        """
        If require.database is called, ensure that the template,
        encoding and locale parameters are passed through to the
        underlying create_database call
        """
        from fabtools import require
        database_exists.return_value = False
        require.postgres.database('foo', 'bar', locale='some_locale',
            encoding='some_encoding', template='some_template')
        require_locale.assert_called_with('some_locale')
        create_database.assert_called_with('foo', 'bar', locale='some_locale',
            encoding='some_encoding', template='some_template')
