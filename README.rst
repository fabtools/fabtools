Introduction
============

``fabtools`` includes useful functions to help you write your `Fabric <http://fabfile.org/>`_ files.

``fabtools`` makes it easier to manage system users, packages, databases, etc.

``fabtools`` includes a number of low-level actions, as well as a higher level interface called ``require``.

Using ``require`` allows you to use a more declarative style, similar to Chef or Puppet.

Example
=======

Here is an example fabfile using ``fabtools``::

    from fabric.api import *
    from fabtools import require
    import fabtools

    @task
    def setup():

        # Require some Debian/Ubuntu packages
        require.deb.packages([
            'imagemagick',
            'libxml2-dev',
        ])

        # Require a Python package
        with fabtools.python.virtualenv('/home/myuser/env'):
            require.python.package('pyramid')

        # Require an email server
        require.postfix.server('example.com')

        # Require a PostgreSQL server
        require.postgres.server()
        require.postgres.user('myuser', 's3cr3tp4ssw0rd')
        require.postgres.database('myappsdb', 'myuser')

        # Require a supervisor process for our app
        require.supervisor.process('myapp',
            command='/home/myuser/env/bin/gunicorn_paster /home/myuser/env/myapp/production.ini',
            directory='/home/myuser/env/myapp',
            user='myuser'
            )

        # Require an nginx server proxying to our app
        require.nginx.proxied_site('example.com',
            docroot='/home/myuser/env/myapp/myapp/public',
            proxy_url='http://127.0.0.1:8888'
            )

        # Setup a daily cron task
        fabtools.cron.add_daily('maintenance', 'myuser', 'my_script.py')

Supported targets
=================

``fabtools`` currently supports the following target operating systems:

* Ubuntu 10.04 LTS
* Ubuntu 10.10
* Ubuntu 11.04
* Ubuntu 11.10

Tests
=====

Test runner
-----------

If you're using Python 2.7, you can launch the tests using the built-in `unittest <http://docs.python.org/library/unittest.html>`_ runner::

    $ python -m unittest tests

If you're using Python 2.5 or 2.6, you'll need to install `unittest2 <http://pypi.python.org/pypi/unittest2>`_, and use the provided runner::

    $ unit2 tests

Unit tests
----------

Running unit tests requires the `mock <http://pypi.python.org/pypi/mock/>`_ library.

Functional tests
----------------

Running functional tests requires `Vagrant <http://vagrantup.com/>`_ to launch virtual machines,
against which all the tests will be run.

If Vagrant is not installed, the functional tests will be skipped automatically.

If Vagrant is installed, the default is to run the tests on all available base boxes.
You can specify which base boxes should be used by setting the VAGRANT_BOXES environment variable::

    VAGRANT_BOXES='ubuntu_10_04 ubuntu_10_10' python -m unittest tests

You can also use this to manually disable functional tests::

    VAGRANT_BOXES='' python -m unittest tests
