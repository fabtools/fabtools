from __future__ import with_statement

from fabric.api import task


@task
def users():
    """
    Check user creation and modification
    """

    import fabtools

    # create user, without home directory
    fabtools.user.create('user1', create_home=False)
    assert fabtools.user.exists('user1')
    assert not fabtools.files.is_dir('/home/user1')

    # create user, with default home directory
    fabtools.user.create('user2')
    assert fabtools.user.exists('user2')
    assert fabtools.files.is_dir('/home/user2')

    # create user, with custom home directory
    fabtools.user.create('user3', home='/tmp/user3')
    assert fabtools.user.exists('user3')
    assert not fabtools.files.is_dir('/home/user3')
    assert fabtools.files.is_dir('/tmp/user3')


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

    # require that a user exist, with default home directory
    require.user('req2', create_home=True)
    assert fabtools.user.exists('req2')
    assert fabtools.files.is_dir('/home/req2')

    # require that a user exist, with custom home directory
    require.user('req3', home='/tmp/req3')
    assert fabtools.user.exists('req3')
    assert not fabtools.files.is_dir('/home/req3')
    assert fabtools.files.is_dir('/tmp/req3')
