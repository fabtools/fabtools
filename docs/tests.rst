Tests
=====

Running tests
-------------

If you're using Python 2.7, you can launch the tests using the built-in `unittest <http://docs.python.org/library/unittest.html>`_ runner::

    $ python -m unittest discover

If you're using Python 2.5 or 2.6, you'll need to install `unittest2 <http://pypi.python.org/pypi/unittest2>`_, and use the provided runner::

    $ pip install unittest2
    $ unit2 discover

Or you can run the tests on all supported Python versions using `tox <http://pypi.python.org/pypi/tox>`_, which will take care of everything::

    $ pip install tox
    $ tox

Unit tests
----------

Running unit tests requires the `mock <http://pypi.python.org/pypi/mock/>`_ library.

Functional tests
----------------

Running functional tests requires `Vagrant <http://vagrantup.com/>`_ to launch virtual machines,
against which all the tests will be run.

If Vagrant is not installed, the functional tests will be skipped automatically.

If Vagrant is installed, the default is to run the tests on all available base boxes.
You can specify which base boxes should be used by setting the FABTOOLS_TEST_BOXES environment variable::

    $ FABTOOLS_TEST_BOXES='ubuntu_10_04 ubuntu_12_04' tox -e py27

You can also use this to manually disable functional tests::

    $ FABTOOLS_TEST_BOXES='' tox

.. note::

   If you have some issue, start by ``rm .tox -rf``.

| ``test_vagrant.py`` execute all fabric file present in ``fabtools/tests/fabfiles/`` folder.
| If you want execute only some fabric file, you can select its like this :

::

    $ FABTOOLS_TEST_INCLUDE='oracle.py redis.py' python -m unittest discover -v fabtools.tests.test_vagrant

or if you want exclude some fabric file :

::

    $ FABTOOLS_TEST_EXCLUDE='nginx.py git.py' python -m unittest discover -v fabtools.tests.test_vagrant

When you work on fabric file, sometime you want to debug Vagrant VM. To do that, you can disable
Vagrant VM destroy with this :

::

    $ FABTOOLS_TEST_NODESTROY=1 python -m unittest discover -v fabtools.tests.test_vagrant
