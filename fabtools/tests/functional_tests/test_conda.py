import pytest

from fabric.api import run

from fabtools import conda, utils
from fabtools import require


def test_conda_install_and_check():
    assert conda.is_conda_installed() == False
    conda.install_miniconda(keep_installer=True)
    assert conda.is_conda_installed()
    run('rm -rf miniconda')
    assert conda.is_conda_installed() == False
    conda.install_miniconda(prefix='~/myminiconda', keep_installer=True)
    assert conda.get_sysprefix() == utils.abspath('myminiconda')
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


def test_package_installation():
    conda.create_env('test3')
    with conda.env('test3'):
        assert conda.is_installed('six') == False
        conda.install('six')
        assert conda.is_installed('six')


def test_require_conda():
     if conda.is_conda_installed():
         prefix = conda.get_sysprefix()
         run('rm -rf ' + utils.abspath(prefix))
         assert conda.is_conda_installed() == False
     require.conda.conda()
     assert conda.is_conda_installed()


def test_require_env():
    # Env creation without package list:
    assert conda.env_exists('require-env') == False
    require.conda.env('require-env')
    assert conda.env_exists('require-env')
    # Env creation with package list:
    assert conda.env_exists('require-env2') == False
    require.conda.env('require-env2', pkg_list=['python','six'])
    assert conda.env_exists('require-env2')
    with conda.env('require-env2'):
        assert conda.is_installed('six')
    # Requiring packages:
    with conda.env('require-env2'):
        assert conda.is_installed('redis') == False
        assert conda.is_installed('yaml') == False
        assert conda.is_installed('future') == False
        require.conda.package('redis')
        assert conda.is_installed('redis')
        require.conda.packages(['yaml','future'])
        assert conda.is_installed('yaml')
        assert conda.is_installed('future')

