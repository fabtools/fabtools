"""
Idempotent API for managing OpenVZ containers
"""
import os.path

from fabtools.files import is_file
from fabtools.openvz import download_template


def template(name=None, url=None):
    """
    Require an OpenVZ template
    """
    if name is not None:
        filename = '%s.tar.gz' % name
    else:
        filename = os.path.basename(url)

    if not is_file(os.path.join('/var/lib/vz/template/cache', filename)):
        download_template(name, url)
