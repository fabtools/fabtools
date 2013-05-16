from __future__ import with_statement

from fabric.api import run, task


@task
def redis():
    """
    Setup Redis server
    """

    from fabtools import require
    from fabtools.require.redis import VERSION

    require.redis.installed_from_source()

    require.redis.instance('db1', port='6379')

    # Check that we can save RDB file
    res = run('echo SAVE | /opt/redis-%s/redis-cli' % VERSION)
    assert res == 'OK'
