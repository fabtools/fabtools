Tests
=====

Running tests
-------------

Using tox
+++++++++

The preferred way to run tests is to use `tox <https://tox.readthedocs.org/en/latest/>`_.
It will take care of everything and run the tests on all supported Python
versions (each in its own virtualenv) and all target operating systems :

::

    $ pip install -r dev-requirements.txt
    $ tox

Tox will also build the Sphinx documentation, so it will tell you about any
reStructuredText syntax errors.

Extra options after a ``--`` on the command line will be passed to the
`py.test <https://pytest.org/>`_ test runner. For example, to stop immediately
after the first failure:

::

    $ tox -- -x

Or to only run tests whose name matches ``apache``:

::

    $ tox -- -k apache


.. note::

   If tox ever gives you trouble, you can ask it to recreate its virtualenvs
   by using the ``-r`` (or ``--recreate``) option. Alternatively, you can start
   over completely by removing the ``.tox`` directory.

Using py.test
+++++++++++++

If you want to use ``py.test`` directly, you will first need to install the test
dependencies. You will also need to install fabtools itself in *development
mode* (also called *editable mode*):

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

Running functional tests requires `Vagrant <https://vagrantup.com/>`_ and
`VirtualBox <https://www.virtualbox.org>`_ to launch the virtual machines
against which the tests will be run.

If Vagrant is not installed, the functional tests will be skipped automatically
and pytest will show a warning message.

Target boxes
++++++++++++

The default tox configuration will run the functional tests using both
Python 2.6 and 2.7, against a specific list of vagrant boxes. These boxes
will be downloaded from Atlas (formerly Vagrant Cloud) when needed if
they're not already installed on your computer.

================ ==============================================================================
Target OS        Vagrant Box Name
================ ==============================================================================
``centos_6_5``   `chef/centos-6.5     <https://atlas.hashicorp.com/chef/boxes/centos-6.5>`_
``debian_6``     `chef/debian-6.0.10  <https://atlas.hashicorp.com/chef/boxes/debian-6.0.10>`_
``debian_7``     `chef/debian-7.8     <https://atlas.hashicorp.com/chef/boxes/debian-7.8>`_
``debian_8``     `debian/jessie64     <https://atlas.hashicorp.com/debian/boxes/jessie64>`_
``ubuntu_12_04`` `hashicorp/precise64 <https://atlas.hashicorp.com/hashicorp/boxes/precise64>`_
``ubuntu_14_04`` `ubuntu/trusty64     <https://atlas.hashicorp.com/ubuntu/boxes/trusty64>`_
================ ==============================================================================

A tox environment name is the combination of the Python version
(either ``py26`` or ``py27``) and a target operating system.

You can use ``tox -l`` to get the list of all test environments.

You can use the ``-e`` option to run tests in one or more specific
environments. For example, you could run the tests using Python 2.7
only, against both Ubuntu 12.04 and 14.04 boxes ::

    $ tox -e py27-ubuntu_12_04,py27-ubuntu_14_04

Skipping the functional tests
+++++++++++++++++++++++++++++

To run the unit tests only, you can use the ``none`` target:

::

    $ tox -e py26-none,py27-none

Using a specific Vagrant box
++++++++++++++++++++++++++++

If you want to run the tests with a specific Vagrant box, you can use
the ``FABTOOLS_TEST_BOX`` environment variable and the ``none`` target::

    $ export FABTOOLS_TEST_BOX='mybox'
    $ tox -e py27-none

Using a specific Vagrant provider
+++++++++++++++++++++++++++++++++

If you want to run the tests with a specific Vagrant provider, you can use
the ``FABTOOLS_TEST_PROVIDER`` environment variable::

    $ export FABTOOLS_TEST_BOX='vmware_box'
    $ export FABTOOLS_TEST_PROVIDER='vmware_fusion'
    $ tox -e py27-none

Debugging functional tests
++++++++++++++++++++++++++

When you're working on a functional test, sometimes you'll want to manually inspect
the state of the Vagrant VM. To do that, you can prevent it from being destroyed
at the end of the test run by using the ``FABTOOLS_TEST_REUSE_VM`` environment
variable:

::

    $ export FABTOOLS_TEST_REUSE_VM=1
    $ tox -e py27-ubuntu_14_04 -- -x -k apache
    $ cd fabtools/tests/functional_tests
    $ vagrant ssh
