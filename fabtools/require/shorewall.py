"""
Shorewall firewall
==================
"""

from fabric.api import hide, puts, settings, shell_env
from fabric.contrib.files import sed

from fabtools.files import watch
from fabtools.service import start, stop, restart
from fabtools.shorewall import (
    Ping,
    SSH,
    HTTP,
    HTTPS,
    SMTP,
    is_started,
    is_stopped,
)
from fabtools.system import UnsupportedFamily, distrib_family

from fabtools.require.deb import package as require_deb_package
from fabtools.require.files import file


DEFAULT_ZONES = [
    {
        'name': 'fw',
        'type': 'firewall',
    },
    {
        'name': 'net',
        'type': 'ipv4',
    },
]

ZONE_HEADER = '#ZONE\tTYPE\tOPTIONS\tIN OPTIONS\tOUT OPTIONS\n'

ZONE_FORMAT = '%(name)s\t%(type)s\t%(options)s\t%(in_options)s\t%(out_options)s\n'


def _zone_config(zones):
    """
    Zone configuration
    """
    if zones is None:
        zones = DEFAULT_ZONES

    lines = [ZONE_HEADER]
    for entry in zones:
        entry.setdefault('options', '')
        entry.setdefault('in_options', '')
        entry.setdefault('out_options', '')
        lines.append(ZONE_FORMAT % entry)

    file('/etc/shorewall/zones', contents=''.join(lines), use_sudo=True)


DEFAULT_INTERFACES = [
    {
        'zone': 'net',
        'interface': 'eth0',
    },
]

INTERFACES_HEADER = '#ZONE\tINTERFACE\tBROADCAST\tOPTIONS\n'

INTERFACES_FORMAT = '%(zone)s\t%(interface)s\t%(broadcast)s\t%(options)s\n'


def _interfaces_config(interfaces):
    """
    Interfaces configuration
    """
    if interfaces is None:
        interfaces = DEFAULT_INTERFACES

    lines = [INTERFACES_HEADER]
    for entry in interfaces:
        entry.setdefault('zone', 'net')
        entry.setdefault('broadcast', 'detect')
        entry.setdefault('options', '')
        lines.append(INTERFACES_FORMAT % entry)

    file('/etc/shorewall/interfaces', contents=''.join(lines), use_sudo=True)


DEFAULT_POLICY = [
    {
        'source': '$FW',
        'dest': 'net',
        'policy': 'ACCEPT',
    },
    {
        'source': 'net',
        'dest': 'all',
        'policy': 'DROP',
        'log_level': 'info',
    },
    {
        'source': 'all',
        'dest': 'all',
        'policy': 'REJECT',
        'log_level': 'info',
    },
]

POLICY_HEADER = '''\
#SOURCE\tDEST\tPOLICY\tLOG  \tBURST:LIMIT
#      \t    \t      \tLEVEL
'''

POLICY_FORMAT = '%(source)s\t%(dest)s\t%(policy)s\t%(log_level)s\t%(burst_limit)s\n'


def _policy_config(policy):
    """
    Policy configuration
    """
    if policy is None:
        policy = DEFAULT_POLICY

    lines = [POLICY_HEADER]
    for entry in policy:
        entry.setdefault('log_level', '')
        entry.setdefault('burst_limit', '')
        lines.append(POLICY_FORMAT % entry)

    file('/etc/shorewall/policy', contents=''.join(lines), use_sudo=True)


DEFAULT_RULES = [
    Ping(),
    SSH(),
    HTTP(),
    HTTPS(),
    SMTP(port=[25, 587]),
]


RULES_HEADER = '''\
#ACTION\tSOURCE\tDEST\tPROTO\tDEST   \tSOURCE \tORIG\tRATE \tUSER/\tMARK\tCONN \tTIME
#      \t      \t    \t     \tPORT(S)\tPORT(S)\tDEST\tLIMIT\tGROUP\t    \tLIMIT
'''

RULES_FORMAT = '%(action)s\t%(source)s\t%(dest)s\t%(proto)s\t%(dest_port)s\t%(source_port)s\t%(original_dest)s\t%(rate_limit)s\t%(user)s\t%(mark)s\t%(conn_limit)s\t%(time)s\n'


def _rules_config(rules):
    """
    Policy configuration
    """
    if rules is None:
        rules = DEFAULT_RULES

    lines = [RULES_HEADER]
    for entry in rules:
        entry.setdefault('proto', 'tcp')
        entry.setdefault('dest_port', '-')
        entry.setdefault('source_port', '-')
        entry.setdefault('original_dest', '-')
        entry.setdefault('rate_limit', '-')
        entry.setdefault('user', '-')
        entry.setdefault('mark', '-')
        entry.setdefault('conn_limit', '-')
        entry.setdefault('time', '-')

        if isinstance(entry['dest_port'], list):
            entry['dest_port'] = ','.join(map(str, entry['dest_port']))

        if isinstance(entry['source_port'], list):
            entry['source_port'] = ','.join(map(str, entry['source_port']))

        lines.append(RULES_FORMAT % entry)

    file('/etc/shorewall/rules', contents=''.join(lines), use_sudo=True)


ROUTESTOPPED_HEADER = '''\
#INTERFACE\tHOST(S)\tOPTIONS\tPROTO\tDEST   \tSOURCE
#         \t       \t       \t     \tPORT(S)\tPORT(S)
'''

ROUTESTOPPED_FORMAT = '%(interface)s\t%(host)s\t%(options)s\t%(proto)s\t%(dest_port)s\t%(source_port)s\n'


def _routestopped_config(routestopped):
    """
    Routestopped configuration

    This lists the hosts that should be accessible
    when the firewall is stopped or starting.
    """
    if routestopped is None:
        routestopped = []

    lines = [ROUTESTOPPED_HEADER]
    for entry in routestopped:
        entry.setdefault('interface', 'eth0')
        entry.setdefault('host', '0.0.0.0/0')
        entry.setdefault('options', '-')
        entry.setdefault('proto', '-')
        entry.setdefault('dest_port', '-')
        entry.setdefault('source_port', '-')

        if isinstance(entry['host'], list):
            entry['host'] = ','.join(entry['host'])

        if isinstance(entry['options'], list):
            entry['options'] = ','.join(entry['options'])

        lines.append(ROUTESTOPPED_FORMAT % entry)

    file('/etc/shorewall/routestopped', contents=''.join(lines), use_sudo=True)


MASQ_HEADER = '''\
#INTERFACE\tSOURCE\tADDRESS\tPROTO\tPORT(S)
'''

MASQ_FORMAT = '%(interface)s\t%(source)s\t%(address)s\t%(proto)s\t%(port)s\n'


def _masq_config(masq):
    """
    Masquerading/SNAT configuration
    """
    if masq is None:
        masq = []

    lines = [MASQ_HEADER]
    for entry in masq:
        entry.setdefault('interface', 'eth0')
        entry.setdefault('address', '-')
        entry.setdefault('proto', '-')
        entry.setdefault('port', '-')

        if isinstance(entry['source'], list):
            entry['source'] = ','.join(entry['source'])

        lines.append(MASQ_FORMAT % entry)

    file('/etc/shorewall/masq', contents=''.join(lines), use_sudo=True)


CONFIG_FILES = [
    '/etc/shorewall/interfaces',
    '/etc/shorewall/masq',
    '/etc/shorewall/policy',
    '/etc/shorewall/routestopped',
    '/etc/shorewall/rules',
    '/etc/shorewall/zones',
]


def firewall(zones=None, interfaces=None, policy=None, rules=None,
             routestopped=None, masq=None):
    """
    Ensure that a firewall is configured.

    Example::

        from fabtools.shorewall import *
        from fabtools import require

        # We need a firewall with some custom rules
        require.shorewall.firewall(
            rules=[
                Ping(),
                SSH(),
                HTTP(),
                HTTPS(),
                SMTP(),
                rule(port=1234, source=hosts(['example.com'])),
            ]
        )

    """

    family = distrib_family()
    if family != 'debian':
        raise UnsupportedFamily(supported=['debian'])

    require_deb_package('shorewall')

    with watch(CONFIG_FILES) as config:
        _zone_config(zones)
        _interfaces_config(interfaces)
        _policy_config(policy)
        _rules_config(rules)
        _routestopped_config(routestopped)
        _masq_config(masq)

    if config.changed:
        puts("Shorewall configuration changed")
        if is_started():
            restart('shorewall')

    with settings(hide('running'), shell_env()):
        sed('/etc/default/shorewall', 'startup=0', 'startup=1', use_sudo=True)


def started():
    """
    Ensure that the firewall is started.
    """
    if not is_started():
        start('shorewall')


def stopped():
    """
    Ensure that the firewall is stopped.
    """
    if not is_stopped():
        stop('shorewall')
