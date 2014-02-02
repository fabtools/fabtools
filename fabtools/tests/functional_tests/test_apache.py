from __future__ import with_statement

from fabric.api import quiet, run, shell_env

from fabtools.files import is_link
from fabtools.system import distrib_family, set_hostname
from fabtools.tests.vagrant_test_case import VagrantTestCase


def setup_module():
    family = distrib_family()
    if family == 'debian':
        from fabtools.require.deb import nopackage
        from fabtools.require.service import stopped
        stopped('nginx')
        nopackage('nginx')


class TestApache(VagrantTestCase):
    """
    Check apache server, enabling and disabling sites.
    """

    @classmethod
    def setUpClass(cls):
        from fabtools.require.service import started
        from fabtools.require.apache import server

        set_hostname('www.example.com')
        server()
        started('apache2')

    @classmethod
    def tearDownClass(cls):
        with quiet():
            cls._stop_apache()
            cls._uninstall_apache()

    @classmethod
    def _stop_apache(cls):
        from fabtools.require.service import stopped
        stopped('apache2')

    @classmethod
    def _uninstall_apache(cls):
        family = distrib_family()
        if family == 'debian':
            from fabtools.require.deb import nopackage
            nopackage('apache2')

    def test_require_module_disabled(self):
        from fabtools.require.apache import module_disabled
        module_disabled('rewrite')
        assert not is_link('/etc/apache2/mods-enabled/rewrite.load')

    def test_require_module_enabled(self):
        from fabtools.require.apache import module_enabled
        module_enabled('rewrite')
        assert is_link('/etc/apache2/mods-enabled/rewrite.load')

    def test_require_site_disabled(self):
        from fabtools.require.apache import site_disabled
        site_disabled('default')
        assert not is_link('/etc/apache2/sites-enabled/000-default')

    def test_require_site_enabled(self):
        from fabtools.require.apache import site_enabled
        site_enabled('default')
        assert is_link('/etc/apache2/sites-enabled/000-default')

    def test_apache_can_serve_a_web_page(self):
        from fabtools import require

        require.apache.site_disabled('default')

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
