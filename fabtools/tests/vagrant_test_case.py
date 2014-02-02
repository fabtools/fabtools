import unittest

from nose.plugins.attrib import attr


@attr('vagrant')
class VagrantTestCase(unittest.TestCase):
    """
    Base class for Vagrant-based functional tests
    """
