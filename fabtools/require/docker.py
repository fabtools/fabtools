"""
Docker
====

This module provides a docker tools.

"""

from fabric.api import env

from fabtools.system import UnsupportedFamily, distrib_family
from fabtools.utils import run_as_root
from fabtools import files

def  core():
    """
    Require the docker core installation.

    Example::

        from fabtools import require

        require.docker.core()

    """

    from fabtools.require.deb import package as require_deb_package
    from fabtools.require.rpm import package as require_rpm_package

    family = distrib_family()

    # Check if sudo command exists
    if not files.exists('/usr/bin/sudo'):
        raise Exception("Please install the sudo package and execute adduser %s sudo" % env.user)


    if not files.exists('/usr/bin/docker'):
        if family == 'debian':
            require_deb_package('curl')
        elif family == 'redhat':
            require_rpm_package('curl')
        else:
            raise UnsupportedFamily(supported=['debian', 'redhat'])

        # Download docker installation
        run_as_root('curl -sSL https://get.docker.com/ | sh')