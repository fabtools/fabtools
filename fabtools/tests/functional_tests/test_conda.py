import pytest

from fabric.api import quiet, run, shell_env

from fabtools.files import is_link
from fabtools.system import distrib_family, set_hostname
from fabtools import conda

#pytestmark = pytest.mark.network


def test_conda_install_and_check(setup_package):
    assert conda.is_conda_installed() == False
    conda.install_miniconda()
    assert conda.is_conda_installed()


def test_conda_create(setup_package):
    conda.create_env(name='test1', packages=['python=2.7'])
    conda.env_exists(name='test1')
    conda.create_env(prefix='testenvs/test1')
    conda.env_exists(prefix='testenvs/test1')
    conda.env_exists(prefix='testenvs/', name='test1')
    conda.env_exists(prefix='testenvs', name='test1')
