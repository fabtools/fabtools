"""
Fabric tools for managing OpenVZ containers
"""
from fabtools import openvz as vz


class Container(object):
    """
    Object-oriented interface to OpenVZ containers
    """

    def __init__(self, ctid):
        self.ctid = ctid

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def create(self, **kwargs):
        return vz.create(self.ctid, **kwargs)

    def destroy(self):
        return vz.destroy(self.ctid)

    def set(self, **kwargs):
        return vz.set(self.ctid, **kwargs)

    def start(self, **kwargs):
        return vz.start(self.ctid, **kwargs)

    def stop(self, **kwargs):
        return vz.stop(self.ctid, **kwargs)

    def restart(self, **kwargs):
        return vz.restart(self.ctid, **kwargs)

    def status(self):
        return vz.status(self.ctid)

    def running(self):
        return vz.running(self.ctid)

    def exists(self):
        return vz.exists(self.ctid)

    def exec2(self, command):
        return vz.exec2(self.ctid, command)
