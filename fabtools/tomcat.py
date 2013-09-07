"""
Tomcat7
=======

This module provides tools for installing `Tomcat7`_.

.. _Tomcat7: http://tomcat.apache.org/

"""
from __future__ import with_statement

from fabric.api import cd, hide, run, settings
from fabtools.utils import run_as_root
from fabtools.files import is_file, is_dir, is_link

DEFAULT_VERSION = '7.0.42'


def install_from_source(version=DEFAULT_VERSION):
    """
    Install Tomcat7 from source.

    ::

        import fabtools

        # Install Tomcat7
        fabtools.tomcat.install_from_source()

    """
    from fabtools.require import file as require_file
    from fabtools.require.files import directory as require_directory

    major = version[0]
    filename = 'apache-tomcat-%s.tar.gz' % version
    foldername = filename[0:-7]

    with cd('/tmp'):
        if not is_file('/tmp/%s' % filename):
            require_file(url='http://archive.apache.org/dist/tomcat/tomcat-%(major)s/v%(version)s/bin/%(filename)s' % {
                'major': major,
                'version': version,
                'filename': filename,
            })
            run('tar -xzf %s' % filename)

        require_directory('/usr/share/tomcat', mode='755', use_sudo=True)
        run_as_root('mv %s/* /usr/share/tomcat' % foldername)
        # run('rm -rf %s' % filename)
        # run('rm -rf %s' % foldername)

    configure_tomcat()
    start_tomcat()


def configure_tomcat():
    from fabric.contrib.files import append, sed

    startupScript = """
# Tomcat auto-start
#
# description: Auto-starts tomcat
# processname: tomcat
# pidfile: /var/run/tomcat.pid

case $1 in
start)
sh /usr/share/tomcat/bin/startup.sh
;;
stop)
sh /usr/share/tomcat/bin/shutdown.sh
;;
restart)
sh /usr/share/tomcat/bin/shutdown.sh
sh /usr/share/tomcat/bin/startup.sh
;;
esac
exit 0"""

    if not is_file('/etc/init.d/tomcat'):
        append('/etc/init.d/tomcat', startupScript, use_sudo=True)
        run_as_root('chmod 755 /etc/init.d/tomcat')

    if not is_link('/etc/rc1.d/K99tomcat'):
        run_as_root('ln -s /etc/init.d/tomcat /etc/rc1.d/K99tomcat')

    if not is_link('/etc/rc2.d/S99tomcat'):
        run_as_root('ln -s /etc/init.d/tomcat /etc/rc2.d/S99tomcat')


def start_tomcat():
    run_as_root('service tomcat start', pty=False)


def stop_tomcat():
    run_as_root('service tomcat stop')


def version():
    """
    Get the version of currently installed tomcat.

    Returns ``None`` if it is not installed.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        res = run('/usr/share/tomcat/bin/version.sh')
    if res.failed:
        return None
    else:
        return _extract_tomcat_version(res)


def _extract_tomcat_version(tomcat_version_out):
    import re
    """
    Extracts tomcat version in format like '7.0.42'
    from 'tomcat/bin/version.sh' command output.
    """
    match = re.search(r'Server version: (.*)', tomcat_version_out)
    if match is None:
        return None
    version = match.group(1).split('/')[1].strip()
    return version
