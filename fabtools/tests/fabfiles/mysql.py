from __future__ import with_statement

from fabric.api import *
from fabtools import require
import fabtools


@task
def mysql():
    """
    Setup MySQL server, user and database
    """
    require.mysql.server(password='s3cr3t')

    with settings(mysql_user='root', mysql_password='s3cr3t'):

        require.mysql.user('myuser', 'foo')
        assert fabtools.mysql.user_exists('myuser')

        require.mysql.database('mydb', owner='myuser')
        assert fabtools.mysql.database_exists('mydb')
