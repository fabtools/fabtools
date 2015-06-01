import os

from fabric.api import run


from fabtools.files import is_dir
from fabtools.utils import run_as_root


def test_create_user_without_home_directory():

    from fabtools.user import create, exists

    try:
        create('user1', create_home=False)

        assert exists('user1')
        assert not is_dir('/home/user1')

    finally:
        run_as_root('userdel -r user1', warn_only=True)


def test_create_user_with_default_home_directory():

    from fabtools.user import create, exists

    try:
        create('user2')

        assert exists('user2')
        assert is_dir('/home/user2')

    finally:
        run_as_root('userdel -r user2', warn_only=True)


def test_create_user_with_home_directory():

    from fabtools.user import create, exists

    try:
        create('user3', home='/tmp/user3')

        assert exists('user3')
        assert not is_dir('/home/user3')
        assert is_dir('/tmp/user3')

    finally:
        run_as_root('userdel -r user3', warn_only=True)


def test_create_system_user_without_home_directory():

    from fabtools.user import create, exists

    try:
        create('user4', system=True)

        assert exists('user4')
        assert not is_dir('/home/user4')

    finally:
        run_as_root('userdel -r user4', warn_only=True)


def test_create_system_user_with_home_directory():

    from fabtools.user import create, exists

    try:
        create('user5', system=True, create_home=True, home='/var/lib/foo')

        assert exists('user5')
        assert is_dir('/var/lib/foo')

    finally:
        run_as_root('userdel -r user5', warn_only=True)


def test_create_two_users_with_the_same_uid():

    from fabtools.user import create, exists

    create('user6', uid='2000')
    assert exists('user6')

    create('user7', uid='2000', non_unique=True)
    assert exists('user7')

    uid6 = int(run("id -u user6"))
    uid7 = int(run("id -u user7"))
    assert uid7 == uid6 == 2000

    run_as_root('userdel -r user6')
    assert not exists('user6')

    run_as_root('userdel -r user7')
    assert not exists('user7')


def test_require_user_without_home():

    from fabtools.require import user
    from fabtools.user import exists

    try:
        user('req1', create_home=False)

        assert exists('req1')
        assert not is_dir('/home/req1')

        # require again
        user('req1')

    finally:
        run_as_root('userdel -r req1', warn_only=True)


def test_require_user_with_default_home():

    from fabtools.require import user
    from fabtools.user import exists

    try:
        user('req2', create_home=True)

        assert exists('req2')
        assert is_dir('/home/req2')

    finally:
        run_as_root('userdel -r req2', warn_only=True)


def test_require_user_with_custom_home():

    from fabtools.require import user
    from fabtools.user import exists

    try:
        user('req3', home='/home/other')

        assert exists('req3')
        assert not is_dir('/home/req3')
        assert is_dir('/home/other')

    finally:
        run_as_root('userdel -r req3', warn_only=True)


def test_require_user_with_ssh_public_keys():

    from fabtools.user import authorized_keys
    from fabtools.require import user

    try:
        tests_dir = os.path.dirname(os.path.dirname(__file__))
        public_key_filename = os.path.join(tests_dir, 'id_test.pub')

        with open(public_key_filename) as public_key_file:
            public_key = public_key_file.read().strip()

        user('req4', home='/tmp/req4', ssh_public_keys=public_key_filename)

        keys = authorized_keys('req4')
        assert keys == [public_key]

        # let's try add same keys second time
        user('req4', home='/tmp/req4', ssh_public_keys=public_key_filename)

        keys = authorized_keys('req4')
        assert keys == [public_key]

    finally:
        run_as_root('userdel -r req4', warn_only=True)
