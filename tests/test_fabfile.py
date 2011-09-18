import os.path

from fabric.api import *
from nose import with_setup

import fabfile


HOST = 'vagrant@127.0.0.1:2224'
KEYFILE = os.path.join(os.path.dirname(__file__), 'id_rsa_vagrant')


def setup():
    """
    Start the vagrant virtual machine before running tests
    """
    with lcd(os.path.dirname(__file__)):
        local('vagrant up')


def teardown():
    """
    Stop the vagrant virtual machine after running tests
    """
    with lcd(os.path.dirname(__file__)):
        local('vagrant halt')


def setup_mysql():
    """
    Clean up MySQL install before tests
    """
    with settings(hide('running', 'stdout'), host_string=HOST, key_filename=KEYFILE):
        sudo("aptitude remove --assume-yes --purge mysql-server-5.1")
        sudo("rm -rf /var/lib/mysql")


@with_setup(setup_mysql)
def test_mysql():
    """
    Run the 'mysql' task from the fabfile
    """
    with settings(host_string=HOST, key_filename=KEYFILE):
        fabfile.mysql()
