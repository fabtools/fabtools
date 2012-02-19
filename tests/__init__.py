import os
import os.path

from fabric.main import load_fabfile
from . import unit


def load_tests(loader, suite, patterns):
    """
    Custom test loader
    """
    # Add unit tests (import here to avoid circular import)
    suite.addTest(loader.loadTestsFromModule(unit))

    # Try to add vagrant functional tests
    from vagrant import base_boxes, VagrantFunctionTestCase, VagrantTestSuite
    boxes = base_boxes()
    if boxes:
        vagrant_suite = VagrantTestSuite(boxes)

        # Add a test case for each fabric task
        path = os.path.join(os.path.dirname(__file__), 'fabfile.py')
        _, tasks, _ = load_fabfile(path)
        for name, task in tasks.items():
            vagrant_suite.addTest(VagrantFunctionTestCase(task))

        suite.addTest(vagrant_suite)

    return suite
