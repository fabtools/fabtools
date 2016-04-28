import pytest

from pipes import quote
from textwrap import dedent
import posixpath

from fabric.api import quiet, run, shell_env, sudo

from fabtools.files import is_link
from fabtools.system import distrib_family


pytestmark = pytest.mark.network


@pytest.fixture(scope='module', autouse=True)
def check_for_debian_family():
    from fabtools.system import distrib_family
    if distrib_family() != 'debian':
        pytest.skip("Skipping Apache test on non-Debian distrib")


@pytest.fixture(scope='module')
def hostname():
    from fabtools.system import set_hostname
    set_hostname('www.example.com')


@pytest.yield_fixture(scope='module')
def apache(hostname, no_nginx):
    _install_apache()
    yield
    _stop_apache()
    _uninstall_apache()


def _install_apache():
    from fabtools.require.service import started
    from fabtools.require.apache import server
    server()
    started('apache2')


def _stop_apache():
    from fabtools.require.service import stopped
    with quiet():
        stopped('apache2')


def _uninstall_apache():
    family = distrib_family()
    if family == 'debian':
        from fabtools.require.deb import nopackage
        with quiet():
            nopackage('apache2')


@pytest.fixture(scope='module')
def no_nginx():
    _stop_nginx()
    _uninstall_nginx()


def _stop_nginx():
    from fabtools.require.service import stopped
    stopped('nginx')


def _uninstall_nginx():
    family = distrib_family()
    if family == 'debian':
        from fabtools.require.deb import nopackage
        nopackage('nginx')


@pytest.yield_fixture(scope='module')
def example_site():
    from fabtools.require.apache import site as require_site
    from fabtools.require.files import directory as require_directory
    from fabtools.require.files import file as require_file

    site_name = 'example.com'

    site_dir = posixpath.join('/var/www', site_name)
    require_directory(site_dir, use_sudo=True)

    site_homepage = posixpath.join(site_dir, 'index.html')
    require_file(site_homepage, contents="example page", use_sudo=True)

    site_config_path = '/etc/apache2/sites-available/{0}.conf'.format(site_name)
    site_link_path = '/etc/apache2/sites-enabled/{0}.conf'.format(site_name)
    require_file(site_config_path, use_sudo=True)

    require_site(
        site_name,
        template_contents=dedent("""\
            <VirtualHost *:%(port)s>
                ServerName %(hostname)s
                DocumentRoot %(document_root)s
                <Directory %(document_root)s>
                </Directory>
            </VirtualHost>
        """),
        port=80,
        hostname=site_name,
        document_root=site_dir,
    )

    yield site_name

    sudo('rm -rf {0}'.format(quote(site_dir)))
    sudo('rm -f {0}'.format(quote(site_config_path)))
    sudo('rm -f {0}'.format(quote(site_link_path)))


def test_require_module_disabled(apache):
    from fabtools.require.apache import module_disabled
    module_disabled('rewrite')
    assert not is_link('/etc/apache2/mods-enabled/rewrite.load')


def test_require_module_enabled(apache):
    from fabtools.require.apache import module_enabled
    module_enabled('rewrite')
    assert is_link('/etc/apache2/mods-enabled/rewrite.load')


def test_require_site_disabled(apache, example_site):
    from fabtools.require.apache import site_disabled
    site_disabled(example_site)
    assert not is_link('/etc/apache2/sites-enabled/{0}.conf'.format(example_site))


def test_require_site_enabled(apache, example_site):
    from fabtools.require.apache import site_enabled
    site_enabled(example_site)
    assert is_link('/etc/apache2/sites-enabled/{0}.conf'.format(example_site))


def test_apache_can_serve_a_web_page(apache, example_site):

    from fabtools.require.apache import site_enabled, site_disabled

    site_disabled('default')
    site_enabled(example_site)

    with shell_env(http_proxy=''):
        body = run('wget -qO- --header="Host: {0}" http://localhost/'.format(example_site))

    assert body == 'example page'
