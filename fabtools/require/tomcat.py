"""
Tomcat 
============

This module provides tools for installing `Tomcat 7`_

.. _Tomcat 7: http://tomcat.apache.org

"""
from fabtools import tomcat


def installed(version=tomcat.DEFAULT_VERSION):
    """
    Require Tomcat 7 to be installed.

    ::

        from fabtools import require

        require.tomcat.installed()

    """
    if tomcat.version() != version:
        tomcat.install_from_source(version)
