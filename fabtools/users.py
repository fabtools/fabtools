"""
Fabric tools for managing users
"""
from fabric.api import *


def user_exists(name):
    """
    Check if user exists
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        return sudo('getent passwd %(name)s' % locals()).succeeded


def create_user(name, gecos=""):
    """
    Create a new user
    """
    sudo('adduser --disabled-password --gecos "%(gecos)s" %(name)s'
        % locals())
