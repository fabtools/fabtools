"""
Idempotent API for managing users
"""
from fabtools.files import is_file
from fabtools.user import *


def user(name):
    """
    Require a user
    """
    if not exists(name):
        create(name)


def sudoer(username, hosts="ALL", operators="ALL", passwd=False, commands="ALL"):
    """
    Require sudo permissions for a given user
    """
    tags = "PASSWD:" if passwd else "NOPASSWD:"
    spec = "%(username)s %(hosts)s=(%(operators)s) %(tags)s %(commands)s" % locals()
    filename = '/etc/sudoers.d/fabtools-%s' % username
    if is_file(filename):
        sudo('chmod 0640 %(filename)s && rm -f %(filename)s' % locals())
    sudo('echo "%(spec)s" >%(filename)s && chmod 0440 %(filename)s' % locals(), shell=True)
