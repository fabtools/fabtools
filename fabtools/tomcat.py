"""
Tomcat7
=======

This module provides tools for installing `Tomcat7`_.

.. _Tomcat7: http://tomcat.apache.org/

"""
from __future__ import with_statement

# Standard imports
import os

# Fabric imports
from fabric.api import cd, hide, run, settings
from fabtools.utils import run_as_root
from fabtools.files import is_file, is_link, is_dir
from fabric.operations import put

# Default parameters
DEFAULT_VERSION = '7.0.47'
DEFAULT_INSTALLATION_PATH = "/usr/share/tomcat"
DEFAULT_MIRROR = "http://archive.apache.org"


def install_from_source(installation_path=DEFAULT_INSTALLATION_PATH,
                        installation_version=DEFAULT_VERSION,
                        mirror=DEFAULT_MIRROR,
                        overwrite=False):
    """
    Install Tomcat7 from source.

    ::

        import fabtools

        # Install Tomcat7
        fabtools.tomcat.install_from_source()

    """
    from fabtools.require import file as require_file
    from fabtools.require.files import directory as require_directory

    # Tokenize version into parts
    version_tokens = installation_version.split('.')
    version_major = version_tokens[0]

    # Parse the filename and folder
    file_name = 'apache-tomcat-{0}.tar.gz'.format(installation_version)
    folder_name = 'apache-tomcat-{0}'.format(installation_version)

    # Build the distribution in /tmp
    with cd('/tmp'):
        # Make sure we have the tarball downloaded.
        if not is_file(os.path.join('/tmp/', file_name)):
            # Otherwise, download the tarball based on our mirror and version.
            tomcat_url = '{3}/dist/tomcat/tomcat-{0}/v{1}/bin/{2}'\
                .format(version_major,
                        installation_version,
                        file_name,
                        mirror)

            # Ensure the file has been downloaded
            require_file(url=tomcat_url)

        # Extract the file
        run('tar -xzf {0}'.format(file_name))

        # Handle possibility of existing path
        if is_dir(installation_path):
            if overwrite == False:
                # Raise exception as we don't want to overwrite
                raise OSError("Path {0} already exists and overwrite not set."\
                              .format(installation_path))
            else:
                # Otherwise, backup the tomcat path
                backup_installation_path = installation_path + ".backup"
                if is_dir(backup_installation_path):
                    run_as_root("rm -rf {0}".format(backup_installation_path))
                run_as_root("mv {0} {1}".format(installation_path,
                                                backup_installation_path))

        '''
        After all that, let's ensure we have the installation path setup
        properly and place the install.
        '''
        require_directory(installation_path, mode='755', use_sudo=True)
        run_as_root('mv {0}/* {1}'.format(folder_name, installation_path))

        # Now cleanup temp.
        run("rm -rf {0}*".format(file_name))

    # Finally, configure and start Tomcat
    configure_tomcat(installation_path, overwrite=overwrite)
    start_tomcat()


def configure_tomcat(installation_path, overwrite=False):
    from fabric.contrib.files import append

    startup_script = """
# Tomcat auto-start
#
# description: Auto-starts tomcat
# processname: tomcat
# pidfile: /var/run/tomcat.pid

case $1 in
start)
sh {0}/bin/startup.sh
;;
stop)
sh {0}/bin/shutdown.sh
;;
restart)
sh {0}/bin/shutdown.sh
sh {0}/bin/startup.sh
;;
esac
exit 0""".format(installation_path)

    # Check for existing files and overwrite.
    if is_file('/etc/init.d/tomcat'):
        if overwrite == False:
            raise OSError("/etc/init.d/tomcat already exists and not overwriting.")
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
    '''
    Start the Tomcat service.
    '''
    run_as_root('service tomcat start', pty=False)


def stop_tomcat():
    '''
    Stop the Tomcat service.
    '''
    run_as_root('service tomcat stop')


def version(installation_path):
    """
    Get the version of currently installed tomcat.

    Returns ``None`` if it is not installed.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        res = run(os.path.join(installation_path, 'bin/version.sh'))
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
    match_version = match.group(1).split('/')[1].strip()
    return match_version


def deploy_application(war_file, webapp_path=None):
    '''
    Deploy an application into the webapp path for a Tomcat installation.
    '''
    # If no webapp path specified, used default installation.
    if not webapp_path:
        webapp_path = os.path.join(DEFAULT_INSTALLATION_PATH, 'webapps')

    # Now copy our WAR into the webapp path.
    put(local_path=war_file, remote_path=os.path.join(webapp_path, war_file),
        use_sudo=True)
