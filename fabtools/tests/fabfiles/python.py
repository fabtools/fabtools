from __future__ import with_statement

from fabric.api import *
from fabtools import require
import fabtools


@task
def python():
    """
    Check Python package installation
    """
    require.python.virtualenv('/tmp/venv')
    assert fabtools.files.is_dir('/tmp/venv')
    assert fabtools.files.is_file('/tmp/venv/bin/python')

    with fabtools.python.virtualenv('/tmp/venv'):
        require.python.package('fabric')
    assert fabtools.files.is_file('/tmp/venv/bin/fab')
