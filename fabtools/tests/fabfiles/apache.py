from __future__ import with_statement

from fabric.api import (
    shell_env,
    task,
)


@task
def apache():
    """
    Check apache server, enabling and disabling sites.
    """

    from fabric.api import run, sudo
    from fabtools import require
    from fabtools.files import is_link
    from fabtools.system import set_hostname

    set_hostname('www.example.com')

    require.apache.server()

    require.apache.module_disabled('rewrite')
    assert not is_link('/etc/apache2/mods-enabled/rewrite.load')

    require.apache.module_enabled('rewrite')
    assert is_link('/etc/apache2/mods-enabled/rewrite.load')

    require.apache.module_disabled('rewrite')
    assert not is_link('/etc/apache2/mods-enabled/rewrite.load')

    require.apache.site_disabled('default')
    assert not is_link('/etc/apache2/sites-enabled/000-default')

    require.apache.site_enabled('default')
    assert is_link('/etc/apache2/sites-enabled/000-default')

    require.apache.site_disabled('default')
    assert not is_link('/etc/apache2/sites-enabled/000-default')

    run('mkdir -p ~/example.com/')
    run('echo "example page" > ~/example.com/index.html')

    require.apache.site(
        'example.com',
        template_contents="""
<VirtualHost *:%(port)s>
    ServerName %(hostname)s

    DocumentRoot %(document_root)s

    <Directory %(document_root)s>
        Options Indexes FollowSymLinks MultiViews

        AllowOverride All

        Order allow,deny
        allow from all
    </Directory>
</VirtualHost>
        """,
        port=80,
        hostname='www.example.com',
        document_root='/home/vagrant/example.com/',
    )

    with shell_env(http_proxy=''):
        body = run('wget -qO- --header="Host: www.example.com" http://localhost/')

    assert body == 'example page'
