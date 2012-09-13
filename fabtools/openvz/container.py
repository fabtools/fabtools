"""
OpenVZ containers
=================
"""
from fabtools import openvz as vz


class Container(object):
    """
    Object-oriented interface to OpenVZ containers.
    """

    def __init__(self, ctid):
        self.ctid = ctid

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def create(self, **kwargs):
        """
        Create the container.

        Extra args are passed to :py:func:`fabtools.openvz.create`.
        """
        return vz.create(self.ctid, **kwargs)

    def destroy(self):
        """
        Destroy the container.
        """
        return vz.destroy(self.ctid)

    def set(self, **kwargs):
        """
        Set container parameters.

        Extra args are passed to :py:func:`fabtools.openvz.set`.
        """
        return vz.set(self.ctid, **kwargs)

    def start(self, **kwargs):
        """
        Start the container.

        Extra args are passed to :py:func:`fabtools.openvz.start`.
        """
        return vz.start(self.ctid, **kwargs)

    def stop(self, **kwargs):
        """
        Stop the container.

        Extra args are passed to :py:func:`fabtools.openvz.stop`.
        """
        return vz.stop(self.ctid, **kwargs)

    def restart(self, **kwargs):
        """
        Restart the container.

        Extra args are passed to :py:func:`fabtools.openvz.restart`.
        """
        return vz.restart(self.ctid, **kwargs)

    def status(self):
        """
        Get the container's status.
        """
        return vz.status(self.ctid)

    def running(self):
        """
        Check if the container is running.
        """
        return vz.running(self.ctid)

    def exists(self):
        """
        Check if the container exists.
        """
        return vz.exists(self.ctid)

    def exec2(self, command):
        """
        Run a command inside the container.

        ::

            from fabtools.require.openvz import container

            with container('foo') as ct:
                res = ct.exec2('hostname')

        .. warning:: the command will be run as **root**.

        """
        return vz.exec2(self.ctid, command)
