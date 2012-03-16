import fnmatch
import os
import os.path

from fabric.main import load_fabfile


def short_doc(obj):
    """
    Returns the first line of the object's docstring
    """
    if obj.__doc__:
        lines = obj.__doc__.strip(' \n').splitlines()
        if lines:
            return lines[0]
    return None


def load_tests(loader, suite, patterns):
    """
    Custom test loader for functional tests
    """

    # Try to add vagrant functional tests
    from .vagrant import base_boxes, VagrantFunctionTestCase, VagrantTestSuite
    boxes = base_boxes()
    if boxes:
        vagrant_suite = VagrantTestSuite(boxes)

        # Add a test case for each task in each fabfile
        fabfiles = os.path.join(os.path.dirname(__file__), 'fabfiles')
        for filename in sorted(os.listdir(fabfiles)):
            if fnmatch.fnmatch(filename, '[!_]*.py'):
                fabfile = os.path.join(fabfiles, filename)
                _, tasks, _ = load_fabfile(fabfile)
                for task in tasks.values():
                    test = VagrantFunctionTestCase(task,
                        description=short_doc(task))
                    vagrant_suite.addTest(test)

        suite.addTest(vagrant_suite)

    return suite
