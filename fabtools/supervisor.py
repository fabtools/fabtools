"""
Fabric tools for managing supervisor processes
"""
from fabric.api import *
from fabtools.files import upload_template


def reload_config():
    """
    Reload supervisor configuration
    """
    sudo("supervisorctl reload")


def add_process(name, options=None):
    """
    Add a supervisor process
    """
    if options is None:
        options = {}

    upload_template('/etc/supervisor/conf.d/%(name)s.conf' % locals(),
        'supervisor/%(name)s.conf' % locals(),
        context=options,
        use_sudo=True)


def start_process(name):
    """
    Start a supervisor process
    """
    sudo("supervisorctl start %(name)s" % locals())


def stop_process(name):
    """
    Stop a supervisor process
    """
    sudo("supervisorctl stop %(name)s" % locals())


def restart_process(name):
    """
    Restart a supervisor process
    """
    sudo("supervisorctl restart %(name)s" % locals())
