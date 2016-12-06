"""
OpenVZ containers
=================

This module provides high-level tools for managing OpenVZ_ templates
and containers.

.. _OpenVZ: http://openvz.org/

.. warning:: The remote host needs a patched kernel with OpenVZ support.

"""

import os

from fabtools import openvz
from fabtools.files import is_file
from fabtools.openvz.container import Container


def template(name=None, url=None):
    """
    Require an OpenVZ OS template.

    If the OS template is not installed yet, it will be downloaded from
    *url* using :py:func:`~fabtools.openvz.download_template()`::

        from fabtools import require

        # Use custom OS template
        require.openvz.template(url='http://example.com/templates/mybox.tar.gz')

    If no *url* is provided, :py:func:`~fabtools.openvz.download_template()`
    will attempt to download the OS template from the
    `download.openvz.org <http://download.openvz.org/template/precreated/>`_
    repository::

        from fabtools import require

        # Use OS template from http://download.openvz.org/template/precreated/
        require.openvz.template('debian-6.0-x86_64')

    """
    if name is not None:
        filename = '%s.tar.gz' % name
    else:
        filename = os.path.basename(url)

    if not is_file(os.path.join('/var/lib/vz/template/cache', filename)):
        openvz.download_template(name, url)


def container(name, ostemplate, **kwargs):
    """
    Require an OpenVZ container.

    If it does not exist, the container will be created using the
    specified OS template
    (see :py:func:`fabtools.require.openvz.template()`).

    Extra args will be passed to :py:func:`fabtools.openvz.create()`::

        from fabtools import require

        require.openvz.container('foo', 'debian', ipadd='1.2.3.4')

    This function returns a :py:class:`fabtools.openvz.Container`
    object, that can be used to perform further operations::

        from fabtools.require.openvz import container

        ct = container('foo', 'debian')
        ct.set('ipadd', '1.2.3.4')
        ct.start()
        ct.exec2('hostname')

    This function can also be used as a context manager::

        from fabtools.require.openvz import container

        with container('foo', 'debian') as ct:
            ct.set('ipadd', '1.2.3.4')
            ct.start()
            ct.exec2('hostname')

    """
    if not openvz.exists(name):
        ctid = openvz.get_available_ctid()
        openvz.create(ctid, ostemplate=ostemplate, **kwargs)
        openvz.set(ctid, name=name)
    return Container(name)
