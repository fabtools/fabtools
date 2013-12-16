"""
GVM
===========

This module provides tools for installing `GVM`_ : the Groovy enVironment Manager

.. _GVM: http://gvmtool.net/

"""

from fabric.api import run

def install():
    """
    Install dependencies (curl and unzip) and Install GVM

    ::

        import fabtools

        # Install GVM
        fabtools.gvm.install()

    """
    from fabtools.require.deb import packages as require_deb_packages
    from fabtools.require.pkg import packages as require_pkg_packages
    from fabtools.require.rpm import packages as require_rpm_packages
    from fabtools.require.oracle_jdk import installed as java
    from fabtools.system import distrib_family, distrib_codename
    from fabric.contrib.files import sed

    res = run('gvm help', quiet=True)
    if res.failed:
        family = distrib_family()
        packages = ['curl', 'unzip']
        if family == 'debian':
            require_deb_packages(packages)
        elif family == 'redhat':
            require_rpm_packages(packages)
        elif family == 'sun':
            require_pkg_packages(packages)
        else:
            raise NotImplementedError()

        java()

        run('curl -s get.gvmtool.net | bash')
        run('source "~/.gvm/bin/gvm-init.sh"')
        sed('~/.gvm/etc/config', 'gvm_auto_answer=false', 'gvm_auto_answer=true')



def install_candidate(candidate, version=None):
    if version is None:
        cmd = 'gvm install %s' % candidate
    else:
        cmd = 'gvm install %s %s' % (candidate, version)

    run(cmd)
