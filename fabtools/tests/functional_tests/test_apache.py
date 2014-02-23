import pytest

from fabric.api import quiet, run, shell_env

from fabtools.files import is_link
from fabtools.system import distrib_family, set_hostname


pytestmark = pytest.mark.network


@pytest.fixture(scope='module', autouse=True)
def remove_nginx():
    stop_nginx()
    uninstall_nginx()


def stop_nginx():
    from fabtools.require.service import stopped
    stopped('nginx')


def uninstall_nginx():
    family = distrib_family()
    if family == 'debian':
        from fabtools.require.deb import nopackage
        nopackage('nginx')


@pytest.fixture(scope='module')
def apache(request):
    install_apache()
    request.addfinalizer(stop_apache)
    request.addfinalizer(uninstall_apache)


def install_apache():
    from fabtools.require.service import started
    from fabtools.require.apache import server
    set_hostname('www.example.com')
    server()
    started('apache2')


def stop_apache():
    from fabtools.require.service import stopped
    with quiet():
        stopped('apache2')


def uninstall_apache():
    family = distrib_family()
    if family == 'debian':
        from fabtools.require.deb import nopackage
        with quiet():
            nopackage('apache2')


def test_require_module_disabled(apache):
    from fabtools.require.apache import module_disabled
    module_disabled('rewrite')
    assert not is_link('/etc/apache2/mods-enabled/rewrite.load')


def test_require_module_enabled(apache):
    from fabtools.require.apache import module_enabled
    module_enabled('rewrite')
    assert is_link('/etc/apache2/mods-enabled/rewrite.load')


def test_require_site_disabled(apache):
    from fabtools.require.apache import site_disabled
    site_disabled('default')
    assert not is_link('/etc/apache2/sites-enabled/000-default')


def test_require_site_enabled(apache):
    from fabtools.require.apache import site_enabled
    site_enabled('default')
    assert is_link('/etc/apache2/sites-enabled/000-default')


def test_apache_can_serve_a_web_page(apache):

    from fabtools.require.apache import site, site_disabled

    site_disabled('default')

    run('mkdir -p ~/example.com/')
    run('echo "example page" > ~/example.com/index.html')

    site(
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
