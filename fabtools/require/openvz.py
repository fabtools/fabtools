"""
Idempotent API for managing OpenVZ containers
"""
import os.path

from fabtools.files import is_file
from fabtools import openvz
from fabtools.openvz.container import Container


def template(name=None, url=None):
    """
    Require an OpenVZ template
    """
    if name is not None:
        filename = '%s.tar.gz' % name
    else:
        filename = os.path.basename(url)

    if not is_file(os.path.join('/var/lib/vz/template/cache', filename)):
        openvz.download_template(name, url)


def container(name, ostemplate, **kwargs):
    """
    Require an OpenVZ container
    """
    if not openvz.exists(name):
        ctid = openvz.get_available_ctid()
        openvz.create(ctid, ostemplate=ostemplate, **kwargs)
        openvz.set(ctid, name=name)
    return Container(name)
