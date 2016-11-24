"""
Oracle JDK
===========

This module provides tools for installing `Oracle JDK`_

.. _Oracle JDK: http://www.oracle.com/technetwork/java/javase/

"""

from pipes import quote
from textwrap import dedent
import posixpath
import re

from fabric.api import run, cd, settings, hide

from fabtools.files import is_dir, is_link
from fabtools.system import get_arch
from fabtools.utils import run_as_root


DEFAULT_VERSION = '7u25-b15'


def install_from_oracle_site(version=DEFAULT_VERSION):
    """
    Download tarball from Oracle site and install JDK.

    ::

        import fabtools

        # Install Oracle JDK
        fabtools.oracle_jdk.install_from_oracle_site()

    """

    prefix = '/opt'

    release, build = version.split('-')
    major, update = release.split('u')
    if len(update) == 1:
        update = '0' + update

    arch = _required_jdk_arch()

    self_extracting_archive = (major == '6')

    extension = 'bin' if self_extracting_archive else 'tar.gz'
    filename = 'jdk-%(release)s-linux-%(arch)s.%(extension)s' % locals()
    download_path = posixpath.join('/tmp', filename)
    url = 'http://download.oracle.com/otn-pub/java/jdk/'\
          '%(version)s/%(filename)s' % locals()

    _download(url, download_path)

    # Prepare install dir
    install_dir = 'jdk1.%(major)s.0_%(update)s' % locals()
    with cd(prefix):
        if is_dir(install_dir):
            run_as_root('rm -rf %s' % quote(install_dir))

    # Extract
    if self_extracting_archive:
        run('chmod u+x %s' % quote(download_path))
        with cd('/tmp'):
            run_as_root('rm -rf %s' % quote(install_dir))
            run_as_root('./%s' % filename)
            run_as_root('mv %s %s' % (quote(install_dir), quote(prefix)))
    else:
        with cd(prefix):
            run_as_root('tar xzvf %s' % quote(download_path))

    # Set up link
    link_path = posixpath.join(prefix, 'jdk')
    if is_link(link_path):
        run_as_root('rm -f %s' % quote(link_path))
    run_as_root('ln -s %s %s' % (quote(install_dir), quote(link_path)))

    # Remove archive
    run('rm -f %s' % quote(download_path))

    _create_profile_d_file(prefix)


def _download(url, download_path):
    from fabtools.require.curl import command as require_curl_command
    require_curl_command()
    options = " ".join([
        '--header "Cookie: oraclelicense=accept-securebackup-cookie"',
        '--location',
    ])
    run('curl %(options)s %(url)s -o %(download_path)s' % locals())


def _create_profile_d_file(prefix):
    """
    Create profile.d file with Java environment variables set.
    """
    from fabtools.require.files import file as require_file

    require_file(
        '/etc/profile.d/java.sh',
        contents=dedent("""\
            export JAVA_HOME="%s/jdk"
            export PATH="$JAVA_HOME/bin:$PATH"
        """ % prefix),
        mode='0755',
        use_sudo=True,
    )


def version():
    """
    Get the version of currently installed JDK.

    Returns ``None`` if it is not installed.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
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
    system_arch = get_arch()
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
    match = re.search(r'Runtime Environment \(build (.*?)\)', java_version_out)
    if match is None:
        return None
    version, build = match.group(1).split('-')
    release = version.split('_')[0].split('.')[1]
    update = str(int(version.split('_')[1]))
    return '%(release)su%(update)s-%(build)s' % locals()
