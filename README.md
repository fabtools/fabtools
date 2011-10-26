Introduction
============

`fabtools` includes useful functions to help you write your [Fabric](http://fabfile.org/) files.

`fabtools` makes it easier to manage system users, packages, databases, etc.

`fabtools` includes a number of low-level actions, as well as a higher level interface called `icanhaz`.

Using `icanhaz` allows you to use a more declarative style, similar to Chef or Puppet.

Example
=======

Here is an example fabfile using `fabtools`.

```python
from fabric.api import *
from fabtools import icanhaz
import fabtools

@task
def setup():

    # Ensure those Debian/Ubuntu packages are installed
    icanhaz.deb.packages([
        'build-essential',
        'python-dev',
        'supervisor',
    ])

    # Ensure those Python packages are installed
    icanhaz.python.package('pyramid')

    # Ensure we have an email server
    icanhaz.postfix.server('example.com')

    # Ensure we have a PostgreSQL server
    icanhaz.postgres.server()
    icanhaz.postgres.user('myuser', 's3cr3tp4ssw0rd)
    icanhaz.postgres.database('myappsdb', 'myuser')

    # Ensure we have a supervisor process for our app
    icanhaz.supervisor.process('myapp', {
        'command': '/home/myuser/env/bin/gunicorn_paster',
        'config': '/home/myuser/env/myapp/production.ini',
        'directory': '/home/myuser/env/myapp',
        'user': 'myuser',
    })

    # Ensure we have an nginx server proxying to our app
    icanhaz.nginx.server()
    icanhaz.nginx.site('example.com', {
        'aliases': 'www.example.com www2.example.com',
        'docroot': '/home/myuser/env/myapp/myapp/public',
        'proxy_url': 'http://127.0.0.1:8888',
    })

    # Ensure we have a cron task running daily
    fabtools.cron.add_daily('maintenance', 'myuser', 'my_script.py')
```

Supported targets
=================

`fabtools` currently supports the following target operating systems:

* Ubuntu 10.04 LTS
* Ubuntu 10.10

Serious mode
============

If you're not a fan of cutesy names, here is a way to switch to "serious mode" for your fabfiles:

```python
from fabric.api import *
from fabtools import icanhaz as require

@task
def serious_setup():
    require.postgres.server()
    require.postgres.user('myuser', 's3cr3tp4ssw0rd)
    require.postgres.database('myappsdb', 'myuser')
```

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
