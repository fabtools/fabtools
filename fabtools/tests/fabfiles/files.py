from __future__ import with_statement

import os
from tempfile import mkstemp
from functools import partial

from fabric.api import *
from fabtools import require
import fabtools


@task
def files():
    """
    Check file creation
    """
    with cd('/tmp'):
        # Require that a file exists
        require.file('foo')
        assert fabtools.files.is_file('foo')
        assert run('cat foo') == '', run('cat foo')

        # Require that a file exists, whose contents should come from a URL
        require.file(url='http://www.google.com/robots.txt')
        assert fabtools.files.is_file('robots.txt')

        # Require that a file exists, whose contents should be this string
        bar_contents = '''This is the contents of the bar file'''
        require.file('bar', contents=bar_contents)
        assert fabtools.files.is_file('bar')
        assert run('cat bar') == bar_contents, run('cat bar')

        # Require that a file exists, whose contents should be this local file
        baz_contents = '''This is the contents of the bar file'''
        fd, filename = mkstemp()
        tmp_file = os.fdopen(fd, 'w')
        tmp_file.write(baz_contents)
        tmp_file.close()
        require.file('baz', source=filename)
        os.remove(filename)
        assert fabtools.files.is_file('baz')
        assert run('cat baz') == baz_contents, run('cat baz')

        # Ensure that changes to watched file are detected
        require.file('watched', contents='aaa')
        with fabtools.files.watch('watched') as f:
            require.file('watched', contents='bbb')
        assert f.changed
        with fabtools.files.watch('watched') as f:
            pass
        assert not f.changed

        # Ensure that the callable is triggered only
        # when the watched file is modified
        require.file('watched', contents='aaa')
        with fabtools.files.watch('watched', callback=partial(require.file, 'modified1')):
            require.file('watched', contents='bbb')
        assert fabtools.files.is_file('modified1')
        with fabtools.files.watch('watched', callback=partial(require.file, 'modified2')):
            pass
        assert not fabtools.files.is_file('modified2')
