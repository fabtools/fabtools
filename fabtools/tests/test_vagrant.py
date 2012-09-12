import fnmatch
import os
import os.path

from fabric.main import load_fabfile


def load_tests(loader, suite, patterns):
    """
    Custom test loader for functional tests
    """

    # Try to add vagrant functional tests
    from .vagrant import base_boxes, VagrantTestCase, VagrantTestSuite
    boxes = base_boxes()
    if boxes:
        vagrant_suite = VagrantTestSuite(boxes)

        # Add a test case for each task in each fabfile
        fabfiles = os.path.join(os.path.dirname(__file__), 'fabfiles')
        for filename in sorted(os.listdir(fabfiles)):
            if fnmatch.fnmatch(filename, '[!_]*.py'):
                fabfile = os.path.join(fabfiles, filename)
                _, tasks, _ = load_fabfile(fabfile)
                for name, callable in tasks.iteritems():
                    test = VagrantTestCase(name, callable)
                    vagrant_suite.addTest(test)

        suite.addTest(vagrant_suite)

    return suite
