"""
Fabric tools for managing network
"""
from __future__ import with_statement

from fabric.api import *


def interfaces():
    """
    Get the list of network interfaces

        >>> fabtools.network.interfaces()
        ['eth0', 'eth1', 'lo']

    """
    with settings(hide('running', 'stdout')):
        res = run('/sbin/ifconfig -s')
    return map(lambda line: line.split(' ')[0], res.splitlines()[1:])


def address(interface):
    """
    Get the IPv4 address assigned to an interface

        >>> fabtools.network.address('lo')
        '127.0.0.1'

    """
    with settings(hide('running', 'stdout')):
        res = run("/sbin/ifconfig %(interface)s | grep 'inet addr'" % locals())
    return res.split()[1].split(':')[1]


def nameservers():
    """
    Get the list of nameserver addresses

        >>> fabtools.network.nameservers()
        ['208.67.222.222', '208.67.220.220']

    """
    with settings(hide('running', 'stdout')):
        res = run("cat /etc/resolv.conf | grep 'nameserver' | cut -d\  -f2")
    return res.splitlines()
