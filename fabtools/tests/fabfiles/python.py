from __future__ import with_statement

from fabric.api import task


@task
def python_setuptools():
    """
    Test setuptools installation
    """

    from fabtools import require

    require.python.setuptools()


@task
def python_virtualenv():
    """
    Test Python virtualenv creation
    """

    from fabtools import require
    import fabtools

    require.python.virtualenv('/tmp/venv')

    assert fabtools.files.is_dir('/tmp/venv')
    assert fabtools.files.is_file('/tmp/venv/bin/python')


@task
def python_package():
    """
    Test Python package installation
    """

    from fabtools import require
    import fabtools

    require.python.virtualenv('/tmp/venv')
    with fabtools.python.virtualenv('/tmp/venv'):
        require.python.package('fabric')

    assert fabtools.files.is_file('/tmp/venv/bin/fab')
