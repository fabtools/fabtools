import fnmatch
import os
import os.path

from fabric.main import load_fabfile


def load_tests(loader, suite, patterns):
    """
    Custom test loader for functional tests
    """

    # Optional include/exclude list of fabfiles
    include_files = os.environ.get('FABTOOLS_TEST_INCLUDE', '').split()
    exclude_files = os.environ.get('FABTOOLS_TEST_EXCLUDE', '').split()

    # Try to add vagrant functional tests
    from .vagrant import test_boxes, VagrantTestCase, VagrantTestSuite
    boxes = test_boxes()
    if boxes:
        vagrant_suite = VagrantTestSuite(boxes)

        # Add a test case for each task in each fabfile
        fabfiles = os.path.join(os.path.dirname(__file__), 'fabfiles')
        for filename in sorted(os.listdir(fabfiles)):
            if fnmatch.fnmatch(filename, '[!_]*.py'):
                # Skip file if in exclude list
                if filename in exclude_files:
                    continue
                # Skip file if it's not in an explicit include list
                if include_files and filename not in include_files:
                    continue
                fabfile = os.path.join(fabfiles, filename)
                _, tasks, _ = load_fabfile(fabfile)
                for name, callable in tasks.iteritems():
                    test = VagrantTestCase(name, callable)
                    vagrant_suite.addTest(test)

        suite.addTest(vagrant_suite)

    return suite
