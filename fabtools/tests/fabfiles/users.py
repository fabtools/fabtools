from __future__ import with_statement

import os

from fabric.api import run, task


@task
def should_create_user_without_home_directory():

    import fabtools

    fabtools.user.create('user1', create_home=False)

    assert fabtools.user.exists('user1')
    assert not fabtools.files.is_dir('/home/user1')


@task
def should_create_user_with_default_home_directory():

    import fabtools

    fabtools.user.create('user2')

    assert fabtools.user.exists('user2')
    assert fabtools.files.is_dir('/home/user2')


@task
def should_create_user_with_home_directory():

    import fabtools

    fabtools.user.create('user3', home='/tmp/user3')

    assert fabtools.user.exists('user3')
    assert not fabtools.files.is_dir('/home/user3')
    assert fabtools.files.is_dir('/tmp/user3')


@task
def should_create_system_user_without_home_directory():

    import fabtools

    fabtools.user.create('user4', system=True)

    assert not fabtools.files.is_dir('/home/user4')


@task
def should_create_system_user_with_home_directory():

    import fabtools

    fabtools.user.create('user5', system=True,
                         create_home=True, home='/var/lib/foo')

    assert fabtools.files.is_dir('/var/lib/foo')

    # create two user with same uid
    fabtools.user.create('user6', uid='1000', non_unique=True)
    uid6 = int(run("id -u user6"))
    fabtools.user.create('user7', uid='1000', non_unique=True)
    uid7 = int(run("id -u user7"))
    assert 1000 == uid6 == uid7


@task
def require_users():
    """
    Check user creation and modification using fabtools.require
    """

    from fabtools import require
    import fabtools

    # require that a user exist, without home directory
    require.user('req1', create_home=False)
    assert fabtools.user.exists('req1')
    assert not fabtools.files.is_dir('/home/req1')

    # require again
    require.user('req1')

    # require that a user exist, with default home directory
    require.user('req2', create_home=True)
    assert fabtools.user.exists('req2')
    assert fabtools.files.is_dir('/home/req2')

    # require that a user exist, with custom home directory
    require.user('req3', home='/home/other')
    assert fabtools.user.exists('req3')
    assert not fabtools.files.is_dir('/home/req3')
    assert fabtools.files.is_dir('/home/other')


@task
def require_ssh_public_keys():
    """
    Check addition of SSH public key
    """

    from fabtools.user import authorized_keys
    from fabtools import require

    tests_dir = os.path.dirname(os.path.dirname(__file__))
    public_key_filename = os.path.join(tests_dir, 'id_test.pub')

    with open(public_key_filename) as public_key_file:
        public_key = public_key_file.read().strip()

    require.user('req4', home='/tmp/req4', ssh_public_keys=public_key_filename)

    keys = authorized_keys('req4')
    assert keys == [public_key], keys

    # let's try add same keys second time
    require.user('req4', home='/tmp/req4', ssh_public_keys=public_key_filename)

    keys = authorized_keys('req4')
    assert keys == [public_key], keys
