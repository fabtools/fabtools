"""
Fabric tools for managing shorewall
"""
from __future__ import with_statement

from fabric.api import *

from socket import gethostbyname
import re


def status():
    """
    Get the firewall status
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        res = sudo('shorewall status')
    return re.search(r'\nShorewall is (\w+)', res).group(1)


def is_started():
    """
    Returns True if shorewall is started
    """
    return status() == 'running'


def is_stopped():
    """
    Returns True if shorewall is stopped
    """
    return status() == 'stopped'


def hosts(hostnames, zone='net'):
    """
    Builds a host list suitable for use in a firewall rule
    """
    addresses = [gethostbyname(name) for name in hostnames]
    return "%s:%s" % (zone, ','.join(addresses))


def rule(port, action='ACCEPT', source='net', dest='$FW', proto='tcp'):
    """
    Builds a firewall rule
    """
    return {
        'action': action,
        'source': source,
        'dest': dest,
        'proto': proto,
        'dest_port': port,
    }


def Ping(**kwargs):
    """
    Build a firewall rule for ICMP pings
    """
    return rule(port=8, proto='icmp', **kwargs)


def SSH(port=22, **kwargs):
    """
    Build a firewall rule for SSH connections
    """
    return rule(port, **kwargs)


def HTTP(port=80, **kwargs):
    """
    Builds a firewall rule for HTTP connections
    """
    return rule(port, **kwargs)


def HTTPS(port=443, **kwargs):
    """
    Builds a firewall rule for HTTPS connections
    """
    return rule(port, **kwargs)


def SMTP(port=25, **kwargs):
    """
    Builds a firewall rule for SMTP connections
    """
    return rule(port, **kwargs)
