from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestShorewall(VagrantTestCase):

    @classmethod
    def setUpClass(cls):
        from fabtools.require.shorewall import firewall
        import fabtools.shorewall
        firewall(
            rules=[
                fabtools.shorewall.Ping(),
                fabtools.shorewall.SSH(),
                fabtools.shorewall.HTTP(),
                fabtools.shorewall.HTTPS(),
                fabtools.shorewall.SMTP(),
                fabtools.shorewall.rule(
                    port=1234,
                    source=fabtools.shorewall.hosts(['example.com']),
                ),
            ]
        )

    def test_require_firewall_started(self):
        from fabtools.require.shorewall import started
        from fabtools.shorewall import is_started
        started()
        self.assertTrue(is_started())

    def test_require_firewall_stopped(self):
        from fabtools.require.shorewall import stopped
        from fabtools.shorewall import is_stopped
        stopped()
        self.assertTrue(is_stopped())
