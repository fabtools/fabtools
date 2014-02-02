from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestPostgreSQL(VagrantTestCase):
    """
    Setup PostgreSQL server, user and database
    """

    @classmethod
    def setUpClass(cls):
        from fabtools.require.postgres import server
        server()

    @classmethod
    def tearDownClass(cls):
        from fabtools.postgres import database_exists, drop_database, drop_user, user_exists

        if database_exists('pgdb'):
            drop_database('pgdb')

        if user_exists('pguser'):
            drop_user('pguser')

    def test_create_and_drop_user(self):
        from fabtools.postgres import create_user, drop_user, user_exists

        create_user('alice', password='1234')
        self.assertTrue(user_exists('alice'))

        drop_user('alice')
        self.assertFalse(user_exists('alice'))

    def test_require_user(self):
        from fabtools.postgres import user_exists
        from fabtools.require.postgres import user

        user('pguser', 'foo')
        self.assertTrue(user_exists('pguser'))

    def test_require_database(self):
        from fabtools.postgres import database_exists
        from fabtools.require.postgres import user, database

        user('pguser')
        database('pgdb', 'pguser')

        self.assertTrue(database_exists('pgdb'))
