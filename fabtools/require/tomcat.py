"""
Tomcat
============

This module provides tools for installing `Tomcat`_

.. _Tomcat: http://tomcat.apache.org

"""
from fabtools import tomcat


def installed(tomcat_version=tomcat.DEFAULT_VERSION):
    """
    Require Tomcat to be installed.

    ::

        from fabtools import require

        require.tomcat.installed()

    """
    if tomcat.version(tomcat.DEFAULT_INSTALLATION_PATH) != tomcat_version:
        tomcat.install_from_source(installation_version=tomcat_version,
                                   overwrite=True)
