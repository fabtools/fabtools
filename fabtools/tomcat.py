"""
Tomcat7
=======

This module provides tools for installing `Tomcat7`_.

.. _Tomcat7: http://tomcat.apache.org/

"""
from __future__ import with_statement

# Fabric imports
from fabric.api import cd, hide, run, settings
from fabtools.utils import run_as_root
from fabtools.files import is_file, is_link

# Default parameters
DEFAULT_VERSION = '7.0.47'
DEFAULT_INSTALLATION_PATH = "/usr/share/tomcat"
DEFAULT_MIRROR = "http://archive.apache.org"


def install_from_source(installation_path=DEFAULT_INSTALLATION_PATH,
                        installation_version=DEFAULT_VERSION,
                        mirror=DEFAULT_MIRROR):
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
        if not is_file('/tmp/{0}'.format(file_name)):
            # Ensure that the archive is in the right place
            tomcat_url = '{3}/dist/tomcat/tomcat-{0}/v{1}/bin/{2}'\
                .format(version_major,
                        version,
                        file_name,
                        mirror)

            # Ensure the file has been downloaded
            require_file(url=tomcat_url)

            # Extract the file
            run('tar -xzf {0}'.format(file_name))

        # Ensure the directory and path match
        require_directory(installation_path, mode='755', use_sudo=True)
        run_as_root('mv {0}/* {1}'.format(folder_name, installation_path))
        run("rm -f {0}".format(file_name))

    # Configure and start Tomcat
    configure_tomcat(installation_path)
    start_tomcat()


def configure_tomcat(installation_path):
    from fabric.contrib.files import append

    startupScript = """
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


def version(installation_path):
    """
    Get the version of currently installed tomcat.

    Returns ``None`` if it is not installed.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        res = run('{0}/bin/version.sh'.format(installation_path))
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
