from __future__ import with_statement

from fabric.api import *
from fabtools import require
import fabtools


@task
def postgresql():
    """
    Setup PostgreSQL server, user and database
    """
    require.postgres.server()

    require.postgres.user('pguser', 'foo')
    assert fabtools.postgres.user_exists('pguser')

    require.postgres.database('pgdb', 'pguser')
    assert fabtools.postgres.database_exists('pgdb')
