from __future__ import with_statement

from fabric.api import task


@task
def nginx():
    """
    Check nginx server, enabling and disabling sites.
    """

    from fabtools import require
    from fabtools.files import is_link

    require.nginx.server()

    require.nginx.disabled('default')
    assert not is_link('/etc/nginx/sites-enabled/default')

    require.nginx.enabled('default')
    assert is_link('/etc/nginx/sites-enabled/default')
