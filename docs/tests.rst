Tests
=====

Running tests
-------------

Using tox
+++++++++

The preferred way to run tests is to use `tox <http://pypi.python.org/pypi/tox>`_.
It will take care of everything and run the tests on all supported Python
versions, each in its own virtual environment:

::

    $ pip install tox
    $ tox

You can ask tox to run tests only against specific Python versions like this:

::

    $ tox -e py25
    $ tox -e py26,py27

.. note::

   If tox ever gives you trouble, you can ask it to recreate its virtualenvs
   by using the ``-r`` (or ``--recreate``) option. Alternatively, you can start
   over completely by removing the ``.tox`` directory.

Using unittest
++++++++++++++

Alternatively, if you're using Python 2.7, you can launch the tests using the
built-in `unittest <http://docs.python.org/library/unittest.html>`_ runner::

    $ python -m unittest discover

If you're using Python 2.5 or 2.6, you'll need to install
`unittest2 <http://pypi.python.org/pypi/unittest2>`_ first, then use the
provided ``unit2`` command::

    $ pip install unittest2
    $ unit2 discover


Unit tests
----------

The goal of the unit tests is to test the internal logic of fabtools functions,
without actually running shell commands on a target system.

Running unit tests requires the `mock <http://pypi.python.org/pypi/mock/>`_
library.


Functional tests
----------------

The goal of the functional tests is to test that fabtools functions have the
expected effect when run against a real target system.

Functional tests are ordinary fabfiles, contained in the
``fabtools/tests/fabfiles/`` folder.

Requirements
++++++++++++

Running functional tests requires `Vagrant <http://vagrantup.com/>`_ to launch
virtual machines, against which all the tests will be run.

If Vagrant is not installed, the functional tests will be skipped automatically.

Selecting base boxes
++++++++++++++++++++

If Vagrant is installed, the default is to run the tests on all available base
boxes. You can specify which base boxes should be used by setting the
``FABTOOLS_TEST_BOXES`` environment variable::

    $ FABTOOLS_TEST_BOXES='ubuntu_10_04 ubuntu_12_04' tox -e py27

You can also use this to manually disable functional tests, and run only
the unit tests:

::

    $ FABTOOLS_TEST_BOXES='' tox

Selecting which tests to run
++++++++++++++++++++++++++++

If you only want to execute specific fabfiles during a test run, you can select
them using the ``FABTOOLS_TEST_INCLUDE`` environment variable:

::

    $ FABTOOLS_TEST_INCLUDE='oracle.py redis.py' tox -e py27

If you want to exclude some fabfiles from a test run using the
``FABTOOLS_TEST_EXCLUDE`` environment variable:

::

    $ FABTOOLS_TEST_EXCLUDE='nginx.py git.py' tox -e py27

Debugging functional tests
++++++++++++++++++++++++++

When you're working on a test fabfile, sometimes you'll want to manually inspect
the state of the Vagrant VM. To do that, you can prevent it from being destroyed
at the end of the test run by using the ``FABTOOLS_TEST_NODESTROY`` environment
variable:

::

    $ FABTOOLS_TEST_NODESTROY=1 tox -e py27
    $ cd fabtools/tests
    $ vagrant ssh
