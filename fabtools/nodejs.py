"""
NodeJS environments and packages
================================

Packages are managed with npm.
"""
from fabric.api import run, sudo, cd
from fabtools import require


def install_nodejs(version="0.8.9"):
    """
    Installing Node JS 0.8.9 by default. This script works only for recent
    version of Node JS.
    """
    require.deb.packages([
        'make',
        'openssl',
        'libssl-dev',
        'g++',
    ])

    filename = "node-v{version}.tar.gz".format(locals())
    foldername = filename[0:-7]

    run("wget http://nodejs.org/dist/v%(version)/%(filename)" % locals())
    run("tar -xvzf {}").format(filename)
    with cd(foldername):
        run("./configure ; make")
        sudo("make install")
    run('rm %(filename) ; rm -rf %(foldername)' % locals())

def install(package=None, version=None, global_install=True):
    """
    Install given npm package. If global_install is set to false, package 
    is installed locally.

    If no package is given npm install is run inside current directory
    and install locally all files given by package.json file that should
    be located at the root of curent directory.
    """
    if package:
        if version:
            package += "@{version}".format(version=version)

        if global_install:
            sudo("npm install -g {package}".format(package=package))
        else:
            run("npm install -l {package}".format(package=package))
    else:
        run("npm install")

def update(package, global_install=True):
    """
    update given pack
    """
    if global_install:
        sudo("npm install -g {package}".format(package=package))
    else:
        run("npm install -l {package}".format(package=package))

def uninstall(package, version=None, global_uninstall=True):
    """
    Uninstall given npm package. If global_install is set to false, package 
    is uninstalled locally.
    """
    if version:
        package += "@{version}".format(version=version)

    if global_uninstall:
        sudo("npm uninstall -g {package}".format(package=package))
    else:
        sudo("npm uninstall -l {package}".format(package=package))
