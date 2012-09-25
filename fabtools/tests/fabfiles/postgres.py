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

    # Test low-level operations
    assert not fabtools.postgres.user_exists('alice')
    assert not fabtools.postgres.user_exists('bob')
    fabtools.postgres.create_user('alice', password='1234')
    assert fabtools.postgres.user_exists('alice')
    assert not fabtools.postgres.user_exists('bob')
    fabtools.postgres.create_user('bob', password='5678')
    assert fabtools.postgres.user_exists('alice')
    assert fabtools.postgres.user_exists('bob')

    # Test high-level operations
    require.postgres.user('pguser', 'foo')
    assert fabtools.postgres.user_exists('pguser')

    require.postgres.database('pgdb', 'pguser')
    assert fabtools.postgres.database_exists('pgdb')
