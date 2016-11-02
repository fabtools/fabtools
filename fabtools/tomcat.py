"""
Tomcat
=======

This module provides tools for installing `Tomcat`_.

.. _Tomcat: http://tomcat.apache.org/

"""

import os
import re

from fabric.api import cd, hide, run, settings
from fabric.operations import put

from fabtools.files import is_file, is_link, is_dir
from fabtools.utils import run_as_root


# Default parameters
DEFAULT_VERSION = '7.0.47'
DEFAULT_INSTALLATION_PATH = "/usr/share/tomcat"
DEFAULT_MIRROR = "http://archive.apache.org"


def install_from_source(path=DEFAULT_INSTALLATION_PATH,
                        version=DEFAULT_VERSION,
                        mirror=DEFAULT_MIRROR,
                        overwrite=False):
    """
    Install Tomcat from source.

    ::

        import fabtools

        # Install Tomcat
        fabtools.tomcat.install_from_source(version='6.0.36')

    """
    from fabtools.require import file as require_file
    from fabtools.require.files import directory as require_directory

    # Tokenize version into parts
    version_tokens = version.split('.')
    version_major = version_tokens[0]

    # Parse the filename and folder
    file_name = 'apache-tomcat-%s.tar.gz' % version
    folder_name = 'apache-tomcat-%s' % version

    # Build the distribution in /tmp
    with cd('/tmp'):
        # Make sure we have the tarball downloaded.
        if not is_file(os.path.join('/tmp/', file_name)):
            # Otherwise, download the tarball based on our mirror and version.
            tomcat_url = '%s/dist/tomcat/tomcat-%s/v%s/bin/%s' % (
                mirror, version_major, version, file_name)

            # Ensure the file has been downloaded
            require_file(url=tomcat_url)

        # Extract the file
        run('tar -xzf %s' % file_name)

        # Handle possibility of existing path
        if is_dir(path):
            if overwrite is False:
                # Raise exception as we don't want to overwrite
                raise OSError(
                    "Path %s already exists and overwrite not set." % path)
            else:
                # Otherwise, backup the tomcat path
                backup_installation_path = path + ".backup"
                if is_dir(backup_installation_path):
                    run_as_root("rm -rf %s" % backup_installation_path)
                run_as_root("mv %s %s" % (path, backup_installation_path))

        """
        After all that, let's ensure we have the installation path setup
        properly and place the install.
        """
        require_directory(path, mode='755', use_sudo=True)
        run_as_root('mv %s/* %s' % (folder_name, path))

        # Now cleanup temp.
        run("rm -rf %s*" % file_name)

    # Finally, configure and start Tomcat
    configure_tomcat(path, overwrite=overwrite)
    start_tomcat()


def configure_tomcat(path, overwrite=False):
    from fabric.contrib.files import append
    startup_script = """
#!/bin/sh
### BEGIN INIT INFO
# Provides:          tomcat
# Required-Start:    $local_fs $remote_fs $network $syslog $named
# Required-Stop:     $local_fs $remote_fs $network $syslog $named
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# X-Interactive:     true
# Short-Description: Tomcat
# Description:       Start Tomcat
### END INIT INFO

case $1 in
start)
sh %(path)s/bin/startup.sh
;;
stop)
sh %(path)s/bin/shutdown.sh
;;
restart)
sh %(path)s/bin/shutdown.sh
sh %(path)s/bin/startup.sh
;;
esac
exit 0""" % {'path': path}

    # Check for existing files and overwrite.
    if is_file('/etc/init.d/tomcat'):
        if overwrite is False:
            raise OSError(
                "/etc/init.d/tomcat already exists and not overwriting.")
        else:
            run_as_root("rm -f /etc/init.d/tomcat")

    # Now create the file and symlinks.
    append('/etc/init.d/tomcat', startup_script, use_sudo=True)
    run_as_root('chmod 755 /etc/init.d/tomcat')

    if not is_link('/etc/rc1.d/K99tomcat'):
        run_as_root('ln -s /etc/init.d/tomcat /etc/rc1.d/K99tomcat')

    if not is_link('/etc/rc2.d/S99tomcat'):
        run_as_root('ln -s /etc/init.d/tomcat /etc/rc2.d/S99tomcat')


def start_tomcat():
    """
    Start the Tomcat service.
    """
    run_as_root('/etc/init.d/tomcat start')


def stop_tomcat():
    """
    Stop the Tomcat service.
    """
    run_as_root('/etc/init.d/tomcat stop')


def version(path):
    """
    Get the version of currently installed tomcat.

    Returns ``None`` if it is not installed.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        res = run(os.path.join(path, 'bin/version.sh'))
    if res.failed:
        return None
    else:
        return _extract_tomcat_version(res)


def _extract_tomcat_version(tomcat_version_out):
    """
    Extracts tomcat version in format like '7.0.42'
    from 'tomcat/bin/version.sh' command output.
    """
    match = re.search(r'Server version: (.*)', tomcat_version_out)
    if match is None:
        return None
    match_version = match.group(1).split('/')[1].strip()
    return match_version


def deploy_application(war_file, webapp_path=None):
    """
    Deploy an application into the webapp path for a Tomcat installation.
    """
    # If no webapp path specified, used default installation.
    if not webapp_path:
        webapp_path = os.path.join(DEFAULT_INSTALLATION_PATH, 'webapps')

    # Now copy our WAR into the webapp path.
    put(
        local_path=war_file, remote_path=os.path.join(webapp_path, war_file),
        use_sudo=True)
