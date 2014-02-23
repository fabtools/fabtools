from pipes import quote
import functools
import posixpath

import pytest

from fabric.api import run

from fabtools.files import is_dir, is_file


pytestmark = pytest.mark.network


def test_require_setuptools():
    """
    Test Python setuptools installation
    """

    from fabtools.require.python import setuptools

    setuptools()

    assert run('easy_install --version', warn_only=True).succeeded


def test_require_virtualenv():
    """
    Test Python virtualenv creation
    """

    from fabtools.require.python import virtualenv

    try:
        virtualenv('/tmp/venv')

        assert is_dir('/tmp/venv')
        assert is_file('/tmp/venv/bin/python')

    finally:
        run('rm -rf /tmp/venv')


@pytest.fixture
def venv(request):
    from fabtools.require.python import virtualenv
    path = '/tmp/venv'
    virtualenv(path)
    request.addfinalizer(functools.partial(run, 'rm -rf %s' % quote(path)))
    return path


def test_require_python_package(venv):
    """
    Test Python package installation
    """

    from fabtools import require
    import fabtools

    with fabtools.python.virtualenv(venv):
        require.python.package('fabric')

    assert is_file(posixpath.join(venv, 'bin/fab'))
