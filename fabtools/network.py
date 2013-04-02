"""
Network
=======
"""
from __future__ import with_statement

from fabric.api import hide, run, settings, sudo
from fabtools.files import is_file


def interfaces():
    """
    Get the list of network interfaces. Will return all datalinks on SmartOS.
    """
    with settings(hide('running', 'stdout')):
        if is_file('/usr/sbin/dladm'):
            res = run('/usr/sbin/dladm show-link')
        else:
            res = sudo('/sbin/ifconfig -s')
    return map(lambda line: line.split(' ')[0], res.splitlines()[1:])


def address(interface):
    """
    Get the IPv4 address assigned to an interface.

    Example::

        import fabtools

        # Print all configured IP addresses
        for interface in fabtools.network.interfaces():
            print(fabtools.network.address(interface))

    """
    with settings(hide('running', 'stdout')):
        res = sudo("/sbin/ifconfig %(interface)s | grep 'inet '" % locals())
    if 'addr' in res:
        return res.split()[1].split(':')[1]
    else:
        return res.split()[1]


def nameservers():
    """
    Get the list of nameserver addresses.

    Example::

        import fabtools

        # Check that all name servers are reachable
        for ip in fabtools.network.nameservers():
            run('ping -c1 %s' % ip)

    """
    with settings(hide('running', 'stdout')):
        res = run(r"cat /etc/resolv.conf | grep 'nameserver' | cut -d\  -f2")
    return res.splitlines()
