"""
Oracle JDK
===========

This module provides tools for installing `Oracle JDK`_

.. _Oracle JDK: http://www.oracle.com/technetwork/java/javase/

"""
from __future__ import with_statement
import re

from fabric.api import run, cd, settings, hide

from fabtools import system
from fabtools.require.files import directory as require_directory
from fabtools.require.files import file as require_file
from fabtools.utils import run_as_root

DEFAULT_VERSION = '7u13-b20'


def install_from_oracle_site(version=DEFAULT_VERSION):
    """
    Download tarball from Oracle site and install JDK.

    ::

        import fabtools

        # Install Oracle JDK
        fabtools.oralce_jdk.install_from_oracle_site()

    """

    release, build = version.split('-')
    major, update = release.split('u')
    if len(update) == 1:
        update = '0' + update

    jdk_arch = _required_jdk_arch()

    jdk_filename = 'jdk-%(release)s-linux-%(jdk_arch)s.tar.gz' % locals()
    jdk_dir = 'jdk1.%(major)s.0_%(update)s' % locals()

    jdk_url = 'http://download.oracle.com/otn-pub/java/jdk/' +\
              '%(version)s/%(jdk_filename)s' % locals()

    with cd('/tmp'):
        run('rm -rf %s' % jdk_filename)
        run('wget --no-cookies --header="Cookie: gpw_e24=a" ' +
            '--progress=dot:mega ' +
            '%(jdk_url)s -O /tmp/%(jdk_filename)s' % locals())

    require_directory('/opt', mode='777', use_sudo=True)
    with cd('/opt'):
        run('tar -xzvf /tmp/%s' % jdk_filename)
        run('ln -s %s jdk' % jdk_dir)

    _create_profile_d_file()


def _create_profile_d_file():
    """
    Create profile.d file with Java environment variables set.
    """
    require_file('/etc/profile.d/java.sh', contents=
                'export JAVA_HOME="/opt/jdk"\n' +
                'export PATH="$JAVA_HOME/bin:$PATH"\n',
                 mode='0755', use_sudo=True)


def version():
    """
    Get the version of currently installed JDK.

    Returns ``None`` if it is not installed.
    """
    with settings(hide('running', 'stdout'), warn_only=True):
        res = run('java -version')
    if res.failed:
        return None
    else:
        return _extract_jdk_version(res)


def _required_jdk_arch():
    """
    Returns required JDK architecture for current system
    in format used in Oracle JDK packages: x64 or i586.

    Raises exception when current system architecture is unsupported.
    """
    system_arch = system.get_arch()
    if system_arch == 'x86_64':
        return 'x64'
    elif re.match('i[0-9]86', system_arch):
        return 'i586'
    else:
        raise Exception("Unsupported system architecture '%s' for Oracle JDK" %
                        system_arch)


def _extract_jdk_version(java_version_out):
    """
    Extracts JDK version in format like '7u13-b20'
    from 'java -version' command output.
    """
    re_build = re.search('Runtime Environment \(build (.*?)\)',
                         java_version_out).group(1)
    version, build = re_build.split('-')
    release = version.split('_')[0].split('.')[1]
    update = str(int(version.split('_')[1]))
    return '%(release)su%(update)s-%(build)s' % locals()
