"""
OpenVZ containers
=================
"""

from fabric.api import cd, hide, settings

from fabtools.utils import run_as_root


def create(ctid, ostemplate=None, config=None, private=None,
           root=None, ipadd=None, hostname=None, **kwargs):
    """
    Create an OpenVZ container.
    """
    return _vzctl('create', ctid, ostemplate=ostemplate, config=config,
                  private=private, root=root, ipadd=ipadd, hostname=hostname,
                  **kwargs)


def destroy(ctid_or_name):
    """
    Destroy the container.
    """
    return _vzctl('destroy', ctid_or_name)


def set(ctid_or_name, save=True, **kwargs):
    """
    Set container parameters.
    """
    return _vzctl('set', ctid_or_name, save=save, **kwargs)


def start(ctid_or_name, wait=False, force=False, **kwargs):
    """
    Start the container.

    If *wait* is ``True``, wait until the container is up and running.

    .. warning:: ``wait=True`` is broken with vzctl 3.0.24
                 on Debian 6.0 (*squeeze*)
    """
    return _vzctl('start', ctid_or_name, wait=wait, force=force, **kwargs)


def stop(ctid_or_name, fast=False, **kwargs):
    """
    Stop the container.
    """
    return _vzctl('stop', ctid_or_name, fast=fast, **kwargs)


def restart(ctid_or_name, wait=True, force=False, fast=False, **kwargs):
    """
    Restart the container.
    """
    return _vzctl('restart', ctid_or_name, wait=wait, force=force, fast=fast,
                  **kwargs)


def status(ctid_or_name):
    """
    Get the status of the container.
    """
    with settings(warn_only=True):
        return _vzctl('status', ctid_or_name)


def running(ctid_or_name):
    """
    Check if the container is running.
    """
    return status(ctid_or_name).split(' ')[4] == 'running'


def exists(ctid_or_name):
    """
    Check if the container exists.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        return status(ctid_or_name).succeeded


def exec2(ctid_or_name, command):
    """
    Run a command inside the container.

    ::

        import fabtools

        res = fabtools.openvz.exec2('foo', 'hostname')

    .. warning:: the command will be run as **root**.

    """
    return run_as_root("vzctl exec2 %s '%s'" % (ctid_or_name, command))


def _vzctl(command, ctid_or_name, **kwargs):
    args = _expand_args(**kwargs)
    return run_as_root('vzctl %s %s %s' % (command, ctid_or_name, args))


def _expand_args(**kwargs):
    args = []
    for k, v in kwargs.items():
        if isinstance(v, bool):
            if v is True:
                args.append('--%s' % k)
        elif isinstance(v, (list, tuple)):
            for elem in v:
                args.append('--%s %s' % (k, elem))
        elif v is not None:
            args.append('--%s %s' % (k, v))
    return ' '.join(args)


def download_template(name=None, url=None):
    """
    Download an OpenVZ template.

    Example::

        from fabtools.openvz import download_template

        # Use custom OS template
        download_template(url='http://example.com/templates/mybox.tar.gz')

    If no *url* is provided, the OS template will be downloaded from the
    `download.openvz.org <http://download.openvz.org/template/precreated/>`_
    repository::

        from fabtools.openvz import download_template

        # Use OS template from http://download.openvz.org/template/precreated/
        download_template('debian-6.0-x86_64')

    """
    if url is None:
        url = 'http://download.openvz.org/template/precreated/%s.tar.gz' % name

    with cd('/var/lib/vz/template/cache'):
        run_as_root('wget --progress=dot:mega "%s"' % url)


def list_ctids():
    """
    Get the list of currently used CTIDs.
    """
    with settings(hide('running', 'stdout')):
        res = run_as_root('vzlist -a -1')
    return map(int, res.splitlines())


def get_available_ctid():
    """
    Get an available CTID.
    """
    current_ctids = list_ctids()
    if current_ctids:
        return max(current_ctids) + 1
    else:
        return 1000
