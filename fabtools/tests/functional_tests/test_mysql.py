from __future__ import with_statement

from fabric.api import settings, with_settings

from fabtools import require
from fabtools.tests.vagrant_test_case import VagrantTestCase
import fabtools


class TestMySQLServer(VagrantTestCase):
    """
    Setup MySQL server, user and database
    """

    @classmethod
    def setUpClass(cls):
        require.mysql.server(password='s3cr3t')


class TestCreateMySQLUsers(VagrantTestCase):

    @classmethod
    def setUpClass(cls):
        require.mysql.server(password='s3cr3t')
        with settings(mysql_user='root', mysql_password='s3cr3t'):
            for user, host in [('bob', 'host1'), ('bob', 'host2')]:
                if fabtools.mysql.user_exists(user, host=host):
                    fabtools.mysql.query("DROP USER '%s'@'%s';" % (user, host))

    @with_settings(mysql_user='root', mysql_password='s3cr3t')
    def test_create_user(self):
        fabtools.mysql.create_user('bob', 'password', host='host1')
        fabtools.mysql.create_user('bob', 'password', host='host2')

        self.assertTrue(fabtools.mysql.user_exists('bob', host='host1'))
        self.assertTrue(fabtools.mysql.user_exists('bob', host='host2'))
        self.assertFalse(fabtools.mysql.user_exists('bob', host='localhost'))

        fabtools.mysql.query("DROP USER bob@host1;")
        fabtools.mysql.query("DROP USER bob@host2;")

    @with_settings(mysql_user='root', mysql_password='s3cr3t')
    def test_require_user(self):
        require.mysql.user('myuser', 'foo')

        self.assertTrue(fabtools.mysql.user_exists('myuser'))

        fabtools.mysql.query("DROP USER myuser@localhost;")


class TestCreateMySQLDatabase(VagrantTestCase):

    @classmethod
    def setUpClass(cls):
        require.mysql.server(password='s3cr3t')
        with settings(mysql_user='root', mysql_password='s3cr3t'):
            require.mysql.user('myuser', 'foo')

    @with_settings(mysql_user='root', mysql_password='s3cr3t')
    def test_require_database(self):
        require.mysql.database('mydb', owner='myuser')
        self.assertTrue(fabtools.mysql.database_exists('mydb'))


class TestRunMySQLQueries(VagrantTestCase):

    @classmethod
    def setUpClass(cls):
        require.mysql.server(password='s3cr3t')
        with settings(mysql_user='root', mysql_password='s3cr3t'):
            require.mysql.user('myuser', 'foo')

    @classmethod
    def tearDownClass(cls):
        with settings(mysql_user='root', mysql_password='s3cr3t'):
            fabtools.mysql.query("DROP USER myuser@localhost;")

    def test_run_query_as_a_specific_user(self):
        with settings(mysql_user='myuser', mysql_password='foo'):
            fabtools.mysql.query('select 1;')

    def test_run_query_without_supplying_the_password(self):
        require.file('.my.cnf', contents="[mysql]\npassword=foo")
        with settings(mysql_user='myuser'):
            fabtools.mysql.query('select 2;')
