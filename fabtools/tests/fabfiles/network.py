import socket

from fabric.api import task


def is_valid_ipv4_address(address):
    try:
        _ = socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            _ = socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:    # not a valid address
        return False
    return True


def is_valid_ipv6_address(address):
    try:
        _ = socket.inet_pton(socket.AF_INET6, address)
    except socket.error:    # not a valid address
        return False
    return True


def is_valid_address(address):
    return is_valid_ipv4_address(address) or is_valid_ipv6_address()


@task
def network():
    """
    Test network interfaces
    """

    import fabtools

    interfaces = fabtools.network.interfaces()

    # Check IPv4 addresses
    for interface in interfaces:
        ipv4_address = fabtools.network.address(interface)
        assert is_valid_ipv4_address(ipv4_address), ipv4_address

    # Check loopback interface
    assert 'lo' in interfaces, interfaces
    assert fabtools.network.address('lo') == '127.0.0.1'

    # Check name servers
    for address in fabtools.network.nameservers():
        assert is_valid_address(address), address
