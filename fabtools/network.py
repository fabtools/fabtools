"""
Fabric tools for managing network
"""
from __future__ import with_statement

from fabric.api import *


def address(interface):
    """
    Get IPV4 address assigned to an interface
    """
    with settings(hide('running', 'stdout')):
        return run("/sbin/ifconfig %s | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1 }'" % interface)


def nameservers():
    """
    Get the list of nameserver addresses
    """
    with settings(hide('running', 'stdout')):
        res = run("cat /etc/resolv.conf | grep 'nameserver' | cut -d\  -f2")
    return res.splitlines()
