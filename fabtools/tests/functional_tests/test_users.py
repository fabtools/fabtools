from __future__ import with_statement

import os

from fabric.api import run


from fabtools.files import is_dir

from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestCreateUser(VagrantTestCase):

    def test_create_user_without_home_directory(self):

        from fabtools.user import create, exists

        create('user1', create_home=False)

        self.assertTrue(exists('user1'))
        self.assertFalse(is_dir('/home/user1'))

    def test_create_user_with_default_home_directory(self):

        from fabtools.user import create, exists

        create('user2')

        self.assertTrue(exists('user2'))
        self.assertTrue(is_dir('/home/user2'))

    def test_create_user_with_home_directory(self):

        from fabtools.user import create, exists

        create('user3', home='/tmp/user3')

        self.assertTrue(exists('user3'))
        self.assertFalse(is_dir('/home/user3'))
        self.assertTrue(is_dir('/tmp/user3'))

    def test_create_system_user_without_home_directory(self):

        from fabtools.user import create, exists

        create('user4', system=True)

        self.assertTrue(exists('user4'))
        self.assertFalse(is_dir('/home/user4'))

    def test_create_system_user_with_home_directory(self):

        from fabtools.user import create, exists

        create('user5', system=True, create_home=True, home='/var/lib/foo')

        self.assertTrue(exists('user5'))
        self.assertTrue(is_dir('/var/lib/foo'))

    def test_two_users_with_the_same_uid(self):

        from fabtools.user import create, exists

        create('user6', uid='1000', non_unique=True)
        self.assertTrue(exists('user6'))

        create('user7', uid='1000', non_unique=True)
        self.assertTrue(exists('user7'))

        uid6 = int(run("id -u user6"))
        self.assertEqual(uid6, 1000)

        uid7 = int(run("id -u user7"))
        self.assertEqual(uid7, 1000)


class TestRequireUser(VagrantTestCase):
    """
    Check user creation and modification using fabtools.require
    """

    def test_require_user_without_home(self):

        from fabtools.require import user
        from fabtools.user import exists

        user('req1', create_home=False)

        self.assertTrue(exists('req1'))
        self.assertFalse(is_dir('/home/req1'))

        # require again
        user('req1')

    def test_require_user_with_default_home(self):

        from fabtools.require import user
        from fabtools.user import exists

        user('req2', create_home=True)

        self.assertTrue(exists('req2'))
        self.assertTrue(is_dir('/home/req2'))

    def test_require_user_with_custom_home(self):

        from fabtools.require import user
        from fabtools.user import exists

        user('req3', home='/home/other')

        self.assertTrue(exists('req3'))
        self.assertFalse(is_dir('/home/req3'))
        self.assertTrue(is_dir('/home/other'))

    def test_require_user_with_ssh_public_keys(self):

        from fabtools.user import authorized_keys
        from fabtools.require import user

        tests_dir = os.path.dirname(os.path.dirname(__file__))
        public_key_filename = os.path.join(tests_dir, 'id_test.pub')

        with open(public_key_filename) as public_key_file:
            public_key = public_key_file.read().strip()

        user('req4', home='/tmp/req4', ssh_public_keys=public_key_filename)

        keys = authorized_keys('req4')
        self.assertEqual(keys, [public_key])

        # let's try add same keys second time
        user('req4', home='/tmp/req4', ssh_public_keys=public_key_filename)

        keys = authorized_keys('req4')
        self.assertEqual(keys, [public_key])
