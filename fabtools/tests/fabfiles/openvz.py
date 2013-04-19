from __future__ import with_statement

import time

from fabric.api import cd, local, put, run, settings, sudo, task


@task
def test_openvz():

    import fabtools

    # Skip test if the kernel does not support OpenVZ
    if not fabtools.files.is_dir('/proc/vz'):
        return

    setup_networking()
    setup_containers()


def setup_networking():
    """
    Setup host networking
    """

    setup_nat()
    setup_firewall()


def setup_nat():
    """
    Make sure IP forwarding is enabled
    """

    import fabtools

    fabtools.require.system.sysctl('net.ipv4.ip_forward', 1)


def setup_firewall():
    """
    Shorewall config
    (based on http://www.shorewall.net/OpenVZ.html)
    """

    from fabtools import require

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

    require.shorewall.firewall(
        zones=zones,
        interfaces=interfaces,
        policy=policy,
        masq=masq,
    )

    require.shorewall.started()


def setup_containers():

    from fabtools import require
    from fabtools.openvz import guest, list_ctids
    from fabtools.require.openvz import container
    from fabtools.require.redis import VERSION as REDIS_VERSION
    from fabtools.system import distrib_family
    import fabtools

    if distrib_family() == 'debian':
        require.deb.package('vzctl')

    NAME = 'debian'
    TEMPLATE = 'debian-6.0-x86_64'
    IPADD = '192.168.1.100'
    NAMESERVERS = fabtools.network.nameservers()

    require.openvz.template(TEMPLATE)

    with container(NAME, TEMPLATE, hostname=NAME, ipadd=IPADD) as ct:

        # Make sure the container is started
        if not ct.running():
            ct.start()

        # Set up name servers
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

        # Check run/sudo
        with guest(NAME):
            assert run('whoami') == 'root'
            assert sudo('whoami') == 'root'
            assert sudo('whoami', user='nobody') == 'nobody'

        # Check put
        with guest(NAME):
            local('echo "toto" > /tmp/toto')
            put('/tmp/toto', '/tmp/toto')
            assert run('test -f /tmp/toto').succeeded

        # Run more complex tasks inside container
        with guest(NAME):

            # Check require.file()
            require.file('/tmp/foo')
            assert fabtools.files.is_file('/tmp/foo')

            # Check cd() inside container
            with cd('/tmp'):
                run('touch bar')
                assert fabtools.files.is_file('bar')
            assert fabtools.files.is_file('/tmp/bar')

            # This directory does not exist in the host
            require.directory('/tmp/newdir')
            with cd('/tmp/newdir'):
                run('touch baz')
            assert fabtools.files.is_file('/tmp/newdir/baz')

            # Check that sudo as user works
            with cd('/tmp'):
                sudo('touch tata', user='nobody')
                assert run('stat -c "%U" tata') == 'nobody'

            # Check Debian package install
            fabtools.deb.update_index()
            require.deb.package('htop')
            assert fabtools.files.is_file('/usr/bin/htop')

            # Install Redis
            require.redis.instance('test')
            assert fabtools.files.is_file('/etc/redis/test.conf')
            assert run('echo PING | /opt/redis-%s/redis-cli' % REDIS_VERSION) == 'PONG'

    assert 'debian' in list_ctids()

    # Stop and destroy container
    with container(NAME, TEMPLATE, hostname=NAME, ipadd=IPADD) as ct:
        ct.stop()
        ct.destroy()

    assert 'debian' not in list_ctids()
