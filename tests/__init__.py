import os.path
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from fabric.main import load_fabfile

from vagrant import VagrantFunctionTestCase, VagrantTestSuite


BASE_BOXES = [
    'ubuntu_10_10',
    'ubuntu_10_04',
]


def load_tests(loader, tests, patterns):
    """
    Custom test loader
    """
    suite = VagrantTestSuite(BASE_BOXES)

    # Add a test case for each fabric task
    path = os.path.join(os.path.dirname(__file__), 'fabfile.py')
    _, tasks, _ = load_fabfile(path)
    for name, task in tasks.items():
        suite.addTest(VagrantFunctionTestCase(task))

    return suite


if __name__ == '__main__':
    unittest.main()
