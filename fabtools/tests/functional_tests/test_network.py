import socket

from fabtools.tests.vagrant_test_case import VagrantTestCase


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


class TestNetwork(VagrantTestCase):

    def test_interfaces_ipv4_addresses(self):

        from fabtools.network import interfaces
        from fabtools.network import address

        for interface in interfaces():
            ipv4_address = address(interface)
            self.assertTrue(is_valid_ipv4_address(ipv4_address))

    def test_loopback_interface_exists(self):
        from fabtools.network import interfaces
        self.assertIn('lo', interfaces())

    def test_loopback_interface_address(self):
        from fabtools.network import address
        self.assertEqual(address('lo'), '127.0.0.1')

    def test_name_servers(self):
        from fabtools.network import nameservers
        for address in nameservers():
            self.assertTrue(is_valid_address(address), address)
