Introduction
============

`fabtools` includes useful functions to help you write your [Fabric](http://fabfile.org/) files.

`fabtools` makes it easier to manage system users, packages, databases, etc.

`fabtools` includes a number of low-level actions, as well as a higher level interface called `require`.

Using `require` allows you to use a more declarative style, similar to Chef or Puppet.

Example
=======

Here is an example fabfile using `fabtools`.

```python
from fabric.api import *
from fabtools import require
import fabtools

@task
def setup():

    # Require some Debian/Ubuntu packages
    require.deb.packages([
        'build-essential',
        'python-dev',
        'supervisor',
    ])

    # Require a Python package
    require.python.package('pyramid')

    # Require an email server
    require.postfix.server('example.com')

    # Require a PostgreSQL server
    require.postgres.server()
    require.postgres.user('myuser', 's3cr3tp4ssw0rd)
    require.postgres.database('myappsdb', 'myuser')

    # Require a supervisor process for our app
    require.supervisor.process('myapp', {
        'command': '/home/myuser/env/bin/gunicorn_paster',
        'config': '/home/myuser/env/myapp/production.ini',
        'directory': '/home/myuser/env/myapp',
        'user': 'myuser',
    })

    # Require an nginx server proxying to our app
    require.nginx.server()
    require.nginx.site('example.com', {
        'aliases': 'www.example.com www2.example.com',
        'docroot': '/home/myuser/env/myapp/myapp/public',
        'proxy_url': 'http://127.0.0.1:8888',
    })

    # Setup a daily cron task
    fabtools.cron.add_daily('maintenance', 'myuser', 'my_script.py')
```

Supported targets
=================

`fabtools` currently supports the following target operating systems:

* Ubuntu 10.04 LTS
* Ubuntu 10.10

Tests
=====

The tests use [Vagrant](http://vagrantup.com/) to launch virtual machines,
against which all the tests will be run.

You can launch the tests using the Python 2.7 built-in [unittest](http://docs.python.org/library/unittest.html) runner:

```
$ python -m unittest tests
```

Note that you must have vagrant base boxes named `ubuntu_10_04` and `ubuntu_10_10`
for the tests to work out of the box. You may edit the `BASE_BOXES` list in `tests/__init__.py`
to match your local configuration if necessary.
