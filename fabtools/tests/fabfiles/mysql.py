from __future__ import with_statement

from fabric.api import task, settings


@task
def mysql():
    """
    Setup MySQL server, user and database
    """

    from fabtools import require
    import fabtools

    require.mysql.server(password='s3cr3t')

    with settings(mysql_user='root', mysql_password='s3cr3t'):

        fabtools.mysql.create_user('bob', 'password', host='host1')
        fabtools.mysql.create_user('bob', 'password', host='host2')
        assert fabtools.mysql.user_exists('bob', host='host1')
        assert fabtools.mysql.user_exists('bob', host='host2')
        assert not fabtools.mysql.user_exists('bob', host='localhost')

        require.mysql.user('myuser', 'foo')
        assert fabtools.mysql.user_exists('myuser')

        require.mysql.database('mydb', owner='myuser')
        assert fabtools.mysql.database_exists('mydb')
