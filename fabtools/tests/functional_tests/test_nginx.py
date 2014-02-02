from __future__ import with_statement

from fabtools.system import distrib_family
from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestNginx(VagrantTestCase):
    """
    Check nginx server, enabling and disabling sites.
    """

    @classmethod
    def setUpClass(cls):
        from fabtools.require.nginx import server as require_nginx_server
        require_nginx_server()

    @classmethod
    def tearDownClass(cls):
        family = distrib_family()
        if family == 'debian':
            from fabtools.require.deb import nopackage
            nopackage('nginx')

    def test_site_disabled(self):

        from fabtools.require.nginx import disabled as require_nginx_site_disabled
        from fabtools.files import is_link

        require_nginx_site_disabled('default')
        self.assertFalse(is_link('/etc/nginx/sites-enabled/default'))

    def test_site_enabled(self):

        from fabtools.require.nginx import enabled as require_nginx_site_enabled
        from fabtools.files import is_link

        require_nginx_site_enabled('default')
        self.assertTrue(is_link('/etc/nginx/sites-enabled/default'))
