from __future__ import with_statement

from fabric.api import *
from fabtools import require


@task
def redis():
    """
    Setup Redis server
    """
    require.redis.installed_from_source()

    require.redis.instance('db1', port='6379')
