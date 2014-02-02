from __future__ import with_statement

from fabric.api import run

from fabtools.files import is_file
from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestRedis(VagrantTestCase):

    @classmethod
    def setUpClass(cls):
        from fabtools.require.redis import installed_from_source, instance

        installed_from_source()
        instance('db1', port='6379')

    def test_redis_server_is_installed(self):
        from fabtools.require.redis import VERSION
        self.assertTrue(is_file('/opt/redis-%s/redis-server' % VERSION))

    def test_save_rdb_file(self):
        from fabtools.require.redis import VERSION
        res = run('echo SAVE | /opt/redis-%s/redis-cli' % VERSION)
        self.assertEqual(res, 'OK')
