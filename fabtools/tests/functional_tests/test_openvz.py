from __future__ import with_statement

import time

from fabric.api import cd, local, put, run, settings, sudo

from nose.plugins.skip import SkipTest

from fabtools.files import is_dir, is_file
from fabtools.require import file as require_file
from fabtools.require import directory as require_directory
from fabtools.require.system import sysctl as require_sysctl
from fabtools.tests.vagrant_test_case import VagrantTestCase


def setup_module():
    # Skip this module if the kernel does not support OpenVZ
    if not is_dir('/proc/vz'):
        raise SkipTest("Kernel does not support OpenVZ")


NAME = 'debian'
TEMPLATE = 'debian-6.0-x86_64'
IPADD = '192.168.1.100'


class TestOpenVZ(VagrantTestCase):

    @classmethod
    def setUpClass(cls):
        cls.setup_host_networking()
        cls.setup_containers()

    @classmethod
    def tearDownClass(cls):
        from fabtools.openvz import list_ctids
        from fabtools.require.openvz import container
        with container(NAME, TEMPLATE, hostname=NAME, ipadd=IPADD) as ct:
            ct.stop()
            ct.destroy()
        assert 'debian' not in list_ctids()

    @classmethod
    def setup_host_networking(cls):
        cls.setup_ip_forwarding()
        cls.setup_firewall()

    @classmethod
    def setup_ip_forwarding(cls):
        require_sysctl('net.ipv4.ip_forward', 1)

    @classmethod
    def setup_firewall(cls):
        """
        Shorewall config
        (based on http://www.shorewall.net/OpenVZ.html)
        """

        from fabtools.require.shorewall import firewall, started

        zones = [
            {
                'name': 'fw',
                'type': 'firewall',
            },
            {
                'name': 'net',
                'type': 'ipv4',
            },
            {
                'name': 'vz',
                'type': 'ipv4',
            },
        ]

        interfaces = [
            {
                'zone':      'net',
                'interface': 'eth0',
                'options':   'proxyarp=1',

            },
            {
                'zone':      'vz',
                'interface': 'venet0',
                'options':   'routeback,arp_filter=0',
            },
        ]

        masq = [
            {
                'interface': 'eth0',
                'source':    '192.168.1.0/24',
            }
        ]

        policy = [
            {
                'source': '$FW',
                'dest':   'net',
                'policy': 'ACCEPT',
            },
            {
                'source': '$FW',
                'dest':   'vz',
                'policy': 'ACCEPT',
            },
            {
                'source': 'vz',
                'dest':   'net',
                'policy': 'ACCEPT',
            },
            {
                'source':    'net',
                'dest':      'all',
                'policy':    'DROP',
                'log_level': 'info',
            },
            {
                'source':    'all',
                'dest':      'all',
                'policy':    'REJECT',
                'log_level': 'info',
            },
        ]

        firewall(
            zones=zones,
            interfaces=interfaces,
            policy=policy,
            masq=masq,
        )

        started()

    @classmethod
    def setup_containers(cls):

        from fabtools import require
        from fabtools.require.openvz import container
        from fabtools.system import distrib_family
        import fabtools

        if distrib_family() == 'debian':
            require.deb.package('vzctl')

        require.openvz.template(TEMPLATE)

        with container(NAME, TEMPLATE, hostname=NAME, ipadd=IPADD) as ct:

            # Make sure the container is started
            if not ct.running():
                ct.start()

            # Set up name servers
            NAMESERVERS = fabtools.network.nameservers()
            ct.set(nameserver=NAMESERVERS)

            # Wait until we can ping the container from the host
            with settings(warn_only=True):
                timeout = 0
                while True:
                    if run('ping -c 1 %s' % IPADD).succeeded:
                        break
                    time.sleep(1)
                    timeout += 1
                    assert timeout < 10, "Timeout trying to ping container"

    def test_list_container_ids(self):
        from fabtools.openvz import list_ctids
        self.assertIn('debian', list_ctids())

    def test_run_in_guest_context_manager(self):
        from fabtools.openvz import guest

        with guest(NAME):
            assert run('whoami') == 'root'

    def test_sudo_root_in_guest_context_manager(self):
        from fabtools.openvz import guest

        with guest(NAME):
            assert sudo('whoami') == 'root'

    def test_sudo_nobody_in_guest_context_manager(self):
        from fabtools.openvz import guest

        with guest(NAME):
            assert sudo('whoami', user='nobody') == 'nobody'

    def test_sudo_nobody_file_ownership_in_guest_context_manager(self):
        from fabtools.openvz import guest

        with guest(NAME):
            with cd('/tmp'):
                sudo('touch tata', user='nobody')
                assert run('stat -c "%U" tata') == 'nobody'

    def test_put_in_guest_context_manager(self):
        from fabtools.openvz import guest

        with guest(NAME):
            local('echo "toto" > /tmp/toto')
            put('/tmp/toto', '/tmp/toto')
            assert run('test -f /tmp/toto').succeeded

    def test_require_file_in_guest_context_manager(self):
        from fabtools.openvz import guest

        with guest(NAME):
            require_file('/tmp/foo')
            assert is_file('/tmp/foo')

    def test_cd_in_guest_context_manager(self):
        from fabtools.openvz import guest

        with guest(NAME):
            with cd('/tmp'):
                run('touch bar')
                assert is_file('bar')
            assert is_file('/tmp/bar')

    def test_require_directory_in_guest_context_manager(self):
        from fabtools.openvz import guest

        with guest(NAME):
            require_directory('/tmp/newdir')
            with cd('/tmp/newdir'):
                run('touch baz')
            assert is_file('/tmp/newdir/baz')

    def test_install_debian_package_in_guest_context_manager(self):
        from fabtools.deb import update_index
        from fabtools.openvz import guest
        from fabtools.require.deb import package

        with guest(NAME):
            update_index()
            package('htop')
            assert is_file('/usr/bin/htop')

    def test_install_redis_in_guest_context_manager(self):
        from fabtools.openvz import guest
        from fabtools.require.redis import VERSION, instance

        with guest(NAME):
            instance('test')
            assert is_file('/etc/redis/test.conf')
            assert run('echo PING | /opt/redis-%s/redis-cli' % VERSION) == 'PONG'
