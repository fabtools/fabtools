# -*- coding: utf-8 -*-

"""
Created on 2013-03-04
:author: Andreas Kaiser (disko)
"""

from __future__ import with_statement

import os
from tempfile import mkstemp
from functools import partial

from fabric.api import cd
from fabric.api import run
from fabric.api import task


remote_url = "https://github.com/ronnix/fabtools.git"


@task
def git():
    """ Test low level git tools. """

    from fabtools.git import clone
    from fabtools.git import checkout
    from fabtools.git import pull

    with cd('/tmp'):
        pass
        # clone(remote_url, path=None, use_sudo=False, user=None)
        # pull(path, use_sudo=False, user=None)
        # checkout(path, branch="master", use_sudo=False, user=None)


@task
def git_require():
    """ Test high level git tools. """

    from fabtools.require.git import working_copy

    with cd('/tmp'):
        # working_copy(remote_url, path=None, branch="master", update=True,
        #              use_sudo=False, user=None)

        working_copy(remote_url)
        working_copy(remote_url, path='wc')
        working_copy(remote_url, path='wc', update=False)
        working_copy(remote_url, path='wc', branch="tags/0.11.0")
        working_copy(remote_url, path='wc_root', use_sudo=True)
        working_copy(remote_url, path='wc_nobody', use_sudo=True,
                     user='nobody')
