"""
Idempotent API for managing PostgreSQL users and databases
"""
from fabtools.postgres import *
from fabtools.icanhaz.deb import package
from fabtools.icanhaz.service import started

import re
from distutils.version import StrictVersion

def check_ubuntu_version(issue):
    result=False
    r = re.compile("^Ubuntu ([0-9]*.[0-9]*).*$",re.IGNORECASE).findall(issue)
    if len(r) > 0 : 
        version_string = r[0]
        try:
            result = StrictVersion(version_string) > '10.04'
        except ValueError:
            pass
    return(result)


def server(version='8.4'):
    """
    I can haz PostgreSQL server
    """
    issue = run('echo | cat /etc/issue')
    if check_ubuntu_version(issue):
        package('postgresql')
        started('postgresql')
    else:
        package('postgresql-%s' % version)
        started('postgresql-%s' % version)


def user(name, password):
    """
    I can haz PostgreSQL user
    """
    if not user_exists(name):
        create_user(name, password)


def database(name, owner,postgis=False):
    """
    I can haz PostgreSQL database
    """
    if not database_exists(name):
        create_database(name, owner, postgis)
