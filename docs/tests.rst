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

    $ pip install -r dev-requirements.txt
    $ tox

Tox will also build the Sphinx documentation, so it will tell you about any
reStructuredText syntax errors.

You can ask tox to run tests only against specific Python versions like this:

::

    $ tox -e py27

Extra options after a ``--`` on the command line will be passed to ``py.test``.
For example, to stop immediately after the first failure:

::

    $ tox -e py27 -- -x


.. note::

   If tox ever gives you trouble, you can ask it to recreate its virtualenvs
   by using the ``-r`` (or ``--recreate``) option. Alternatively, you can start
   over completely by removing the ``.tox`` directory.

Using py.test
+++++++++++++

Tox calls ``py.test`` for you, but you may want to use ``py.test`` directly:

::

    $ pip install pytest mock
    $ pip install -e .
    $ py.test

Unit tests
----------

The goal of the unit tests is to test the internal logic of fabtools functions,
without actually running shell commands on a target system.

Most unit tests make use of the `mock <http://pypi.python.org/pypi/mock/>`_
library.


Functional tests
----------------

The goal of the functional tests is to test that fabtools functions have the
expected effect when run against a real target system.

Functional tests are contained in the ``fabtools/tests/functional_tests/`` folder.

Requirements
++++++++++++

Running functional tests requires `Vagrant <http://vagrantup.com/>`_ to launch
virtual machines, against which all the tests will be run.

If Vagrant is not installed, the functional tests will be skipped automatically.

Selecting a base box
++++++++++++++++++++

You can specify which base box should be used as a target by setting the
``FABTOOLS_TEST_BOX`` environment variable::

    $ FABTOOLS_TEST_BOX='hashicorp/precise64' tox -e py27

Selecting a provider
++++++++++++++++++++

If you want to run the tests with a specific Vagrant provider, you can
use the ``FABTOOLS_TEST_PROVIDER`` environment variable::

    $ export FABTOOLS_TEST_PROVIDER='vmware_fusion'
    $ export FABTOOLS_TEST_BOX='somebox'
    $ tox -e py27

Debugging functional tests
++++++++++++++++++++++++++

When you're working on a functional test, sometimes you'll want to manually inspect
the state of the Vagrant VM. To do that, you can prevent it from being destroyed
at the end of the test run by using the ``FABTOOLS_TEST_REUSE_VM`` environment
variable:

::

    $ cd fabtools/tests/functional_tests
    $ export FABTOOLS_TEST_BOX='hashicorp/precise64'
    $ export FABTOOLS_TEST_REUSE_VM=1
    $ py.test -x test_apache.py
    $ vagrant ssh
