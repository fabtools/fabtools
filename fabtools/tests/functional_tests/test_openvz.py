import time

import pytest

from fabric.api import cd, local, put, run, settings, sudo

from fabtools.files import is_dir, is_file
from fabtools.require import file as require_file
from fabtools.require import directory as require_directory
from fabtools.require.system import sysctl as require_sysctl


pytestmark = pytest.mark.network


@pytest.fixture(scope='module', autouse=True)
def check_for_openvz_kernel():
    if not is_dir('/proc/vz'):
        pytest.skip("Kernel does not support OpenVZ")


@pytest.yield_fixture(scope='module')
def container():

    from fabtools.require.openvz import container

    name = 'debian'
    template = 'debian-6.0-x86_64'
    ipadd = '192.168.1.100'

    setup_host_networking()
    setup_container(name, template, ipadd)

    yield name

    with container(name, template, hostname=name, ipadd=ipadd) as ct:
        ct.stop()
        ct.destroy()


def setup_host_networking():
    setup_ip_forwarding()
    setup_firewall()


def setup_ip_forwarding():
    require_sysctl('net.ipv4.ip_forward', 1)


def setup_firewall():
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


def setup_container(name, template, ipadd):

    from fabtools import require
    from fabtools.require.openvz import container
    from fabtools.system import distrib_family
    import fabtools

    if distrib_family() == 'debian':
        require.deb.package('vzctl')

    require.openvz.template(template)

    with container(name, template, hostname=name, ipadd=ipadd) as ct:

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
                if run('ping -c 1 %s' % ipadd).succeeded:
                    break
                time.sleep(1)
                timeout += 1
                assert timeout < 10, "Timeout trying to ping container"


def test_list_container_ids(container):
    from fabtools.openvz import list_ctids
    assert 'debian' in list_ctids()


def test_run_in_guest_context_manager(container):
    from fabtools.openvz import guest

    with guest(container):
        assert run('whoami') == 'root'


def test_sudo_root_in_guest_context_manager(container):
    from fabtools.openvz import guest

    with guest(container):
        assert sudo('whoami') == 'root'


def test_sudo_nobody_in_guest_context_manager(container):
    from fabtools.openvz import guest

    with guest(container):
        assert sudo('whoami', user='nobody') == 'nobody'


def test_sudo_nobody_file_ownership_in_guest_context_manager(container):
    from fabtools.openvz import guest

    with guest(container):
        with cd('/tmp'):
            sudo('touch tata', user='nobody')
            assert run('stat -c "%U" tata') == 'nobody'


def test_put_in_guest_context_manager(container):
    from fabtools.openvz import guest

    with guest(container):
        local('echo "toto" > /tmp/toto')
        put('/tmp/toto', '/tmp/toto')
        assert run('test -f /tmp/toto').succeeded


def test_require_file_in_guest_context_manager(container):
    from fabtools.openvz import guest

    with guest(container):
        require_file('/tmp/foo')
        assert is_file('/tmp/foo')


def test_cd_in_guest_context_manager(container):
    from fabtools.openvz import guest

    with guest(container):
        with cd('/tmp'):
            run('touch bar')
            assert is_file('bar')
        assert is_file('/tmp/bar')


def test_require_directory_in_guest_context_manager(container):
    from fabtools.openvz import guest

    with guest(container):
        require_directory('/tmp/newdir')
        with cd('/tmp/newdir'):
            run('touch baz')
        assert is_file('/tmp/newdir/baz')


def test_install_debian_package_in_guest_context_manager(container):
    from fabtools.deb import update_index
    from fabtools.openvz import guest
    from fabtools.require.deb import package as require_deb_package

    with guest(container):
        update_index()
        require_deb_package('htop')
        assert is_file('/usr/bin/htop')


def test_install_redis_in_guest_context_manager(container):
    from fabtools.openvz import guest
    from fabtools.require.redis import VERSION, instance

    with guest(container):
        instance('test')
        assert is_file('/etc/redis/test.conf')
        assert run('echo PING | /opt/redis-%s/redis-cli' % VERSION) == 'PONG'
