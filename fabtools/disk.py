"""
Disk Tools
===============
"""
from fabric.api import hide, settings, abort
from fabtools.utils import run_as_root

import re


def partition_list(device):
    """
    Get a partition lis for a disk

    Example::

        from fabtools.disk import partition_list

        res = partition_list('/dev/sda')

        return [ ['/dev/sda1','Linux'], ['/dev/sda2','Linux Swap'']]
    """
    # scan partition
    partitions = []
    with settings(hide('running', 'stdout')):
        res = run_as_root('sfdisk -l %(device)s' % locals())

        spart = re.compile(r'(%(device)s[0-9]+) +(\*?) +(.*?) +(.*?) +(.*?) +(.*?) +(.*?) +(.*)' % locals())
        lines = res.splitlines()
        for l in lines:
            m = spart.search(l)
            if m:
                partitions.append([m.group(1), m.group(8)])

    return partitions


def mount(device, mountpoint):
    """
    Mount a partition

    Example::

        from fabtools.disk import mount

        mount('/dev/sdb1','/mnt/usb_drive')
    """
    if not ismounted('%(device)s' % locals()):
        run_as_root('mount %(device)s %(mountpoint)s' % locals())


def swapon(device):
    """
    Active swap partition

    Example::

        from fabtools.disk import swapon

        swapon('/dev/sda1')
    """
    if not ismounted('%(device)s' % locals()):
        run_as_root('swapon %(device)s' % locals())


def ismounted(device):
    """
    Check if partition is mounted

    Example::

        from fabtools.disk import ismounted

        if ismounted('/dev/sda1'):
           print ("disk sda1 is mounted")
    """
    # Check filesystem
    with settings(hide('running', 'stdout')):
        res = run_as_root('mount')
    lines = res.splitlines()
    for l in lines:
        m = re.search('^%(device)s ' % locals(), l)
        if m:
            return True

    # Check swap
    with settings(hide('running', 'stdout')):
        res = run_as_root('swapon -s')
    lines = res.splitlines()
    for l in lines:
        m = re.search('^%(device)s ' % locals(), l)
        if m:
            return True

    return False


def mkfs(device, ftype):
    """
    Format filesystem

    Example::

        from fabtools.disk import mkfs

        mkfs('/dev/sda2', 'ext4')
    """
    if not ismounted('%(device)s' % locals()):
        run_as_root('mkfs.%(ftype)s %(device)s' % locals())
    else:
        abort("Partition is mounted")


def mkswap(device):
    """
    Format swap partition

    Example::

        from fabtools.disk import mkswap

        mkswap('/dev/sda2')
    """
    if not ismounted('%(device)s' % locals()):
        run_as_root('mkswap %(device)s' % locals())
    else:
        abort("swap partition is mounted")


def partition_type_exists(disk, device, ptype):
    """
    Check if partition is a type

    Example::

        from fabtools.disk import partition_type_exists

        if partition_type_exists('/dev/sda', '/dev/sda1', 'Linux'):
           Print ("This is correct for receive a linux install")
    """
    partitions = dict(partition_list(disk))
    search = '%(device)s' % locals()
    if search in partitions:
        return partitions[search] == ptype

    return False
