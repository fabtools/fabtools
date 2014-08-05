import pytest

from fabric.api import quiet, run, shell_env, put

from fabtools.files import is_link
from fabtools.system import distrib_family, set_hostname
from fabtools import conda

#pytestmark = pytest.mark.network


def test_conda_install_and_check():
    assert conda.is_conda_installed() == False
    conda.install_miniconda(keep_installer=True)
    assert conda.is_conda_installed()
    run('rm -rf miniconda')
    assert conda.is_conda_installed() == False
    conda.install_miniconda(prefix='~/myminiconda', keep_installer=True)
    assert conda.is_conda_installed()
    run('rm -rf myminiconda')
    assert conda.is_conda_installed() == False
    conda.install_miniconda(keep_installer=True)


def test_conda_create():
    conda.create_env(name='test1', packages=['python=2.7'])
    conda.env_exists(name='test1')
    conda.create_env(prefix='testenvs/test1')
    conda.env_exists(prefix='testenvs/test1')
    conda.env_exists(prefix='testenvs/', name='test1')
    conda.env_exists(prefix='testenvs', name='test1')


def test_conda_env_decorator():
    conda.create_env(name='test2', packages=['python=2.7'])
    with(conda.env('test2')):
        assert run('python --version 2>&1 | grep -q -e "Python 2.7"').succeeded