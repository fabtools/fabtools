from __future__ import with_statement
import hashlib

from fabric.api import *
import fabtools


@task
def md5():
    """
    Check MD5 sums (unavailable, empty, with content)
    """
    with cd('/tmp'):
        run('touch f1')
        run('echo -n hello > f2')
        assert fabtools.files.md5sum('doesnotexist') is None
        assert fabtools.files.md5sum('f1') == hashlib.md5('').hexdigest()
        assert fabtools.files.md5sum('f2') == hashlib.md5('hello').hexdigest()
