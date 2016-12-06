"""
Shorewall firewall
==================
"""

from socket import gethostbyname
import re

from fabric.api import hide, settings

from fabtools.utils import run_as_root


def status():
    """
    Get the firewall status.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        res = run_as_root('shorewall status')
    return re.search(r'\nShorewall is (\w+)', res).group(1)


def is_started():
    """
    Check if the firewall is started.
    """
    return status() == 'running'


def is_stopped():
    """
    Check if the firewall is stopped.
    """
    return status() == 'stopped'


def hosts(hostnames, zone='net'):
    """
    Builds a host list suitable for use in a firewall rule.
    """
    addresses = [gethostbyname(name) for name in hostnames]
    return "%s:%s" % (zone, ','.join(addresses))


def rule(port, action='ACCEPT', source='net', dest='$FW', proto='tcp'):
    """
    Helper to build a firewall rule.

    Examples::

        from fabtools.shorewall import rule

        # Rule to accept connections from example.com on port 1234
        r1 = rule(port=1234, source=hosts(['example.com']))

        # Rule to reject outgoing SMTP connections
        r2 = rule(port=25, action='REJECT', source='$FW', dest='net')

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
    Helper to build a firewall rule for ICMP pings.

    Extra args will be passed to :py:func:`~fabtools.shorewall.rule`.
    """
    return rule(port=8, proto='icmp', **kwargs)


def SSH(port=22, **kwargs):
    """
    Helper to build a firewall rule for SSH connections

    Extra args will be passed to :py:func:`~fabtools.shorewall.rule`.
    """
    return rule(port, **kwargs)


def HTTP(port=80, **kwargs):
    """
    Helper to build a firewall rule for HTTP connections

    Extra args will be passed to :py:func:`~fabtools.shorewall.rule`.
    """
    return rule(port, **kwargs)


def HTTPS(port=443, **kwargs):
    """
    Helper to build a firewall rule for HTTPS connections

    Extra args will be passed to :py:func:`~fabtools.shorewall.rule`.
    """
    return rule(port, **kwargs)


def SMTP(port=25, **kwargs):
    """
    Helper to build a firewall rule for SMTP connections

    Extra args will be passed to :py:func:`~fabtools.shorewall.rule`.
    """
    return rule(port, **kwargs)
