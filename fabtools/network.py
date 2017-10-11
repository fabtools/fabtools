"""
Network
=======
"""

from fabric.api import hide, run, settings, sudo

from fabtools.files import is_file


def interfaces():
    """
    Get the list of network interfaces. Will return all datalinks on SmartOS.
    """
    with settings(hide('running', 'stdout')):
        if is_file('/usr/sbin/dladm'):
            res = run('/usr/sbin/dladm show-link')
            result = map(lambda line: line.split(' ')[0], res.splitlines()[1:])
        elif is_file('/sbin/ifconfig'):
            res = sudo('/sbin/ifconfig -s')
            result = map(lambda line: line.split(' ')[0], res.splitlines()[1:])
            result.remove('Iface')
        elif is_file('/sbin/ip'):
            res = run('/sbin/ip l')
            res = map(lambda line: line.split(' ')[1], res.splitlines()[1:])
            result = map(lambda line: line.split('@')[0], res)
        else:
            return "Dont have command [dladm|ifconfig|ip]"
    return result

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
        if is_file('/sbin/ifconfig'):
            res = sudo("/sbin/ifconfig %(interface)s | grep 'inet '" % locals())
        else:
            res = run("/sbin/ip a show %(interface)s | grep 'inet '" % locals())
    if interface != "lo" and interface != "":
        if 'addr' in res:
            if 'sudo' in res:
                res = map(lambda line: line.split('addr:')[1], res.splitlines()[1:])
                res = map(lambda line: line.split(' '), res)
                return res[0]
            else:
                return res.split()[1].split(':')[1]
        else:
            return res.split()[1]

def mac(interface):
    """
    Get the MAC address assigned to an interface.

    Example::

        import fabtools

        # Print all configured MAC addresses
        for interface in fabtools.network.interfaces():
            print(fabtools.network.mac(interface))

    """
    with settings(hide('running', 'stdout')):
        res = sudo("/sbin/ifconfig %(interface)s | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'" % locals())
    return res

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
