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
    options['name'] = name

    upload_template('/etc/supervisor/conf.d/%(name)s.conf' % locals(),
        'supervisor/%(name)s.conf' % locals(),
        context=options,
        use_sudo=True)


def process_status(name):
    """
    Get the status of a supervisor process
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo("supervisorctl status %(name)s" % locals())
        if res.startswith("No such process"):
            return None
        else:
            return res.split()[1]


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
