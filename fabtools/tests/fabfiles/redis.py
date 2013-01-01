from __future__ import with_statement

from fabric.api import *


@task
def redis():
    """
    Setup Redis server
    """

    from fabtools import require

    require.redis.installed_from_source()

    require.redis.instance('db1', port='6379')
