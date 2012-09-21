Changelog
=========

Version 0.5.1 (2012-09-21)
--------------------------

* Documentation and packaging fixes

Version 0.5 (2012-09-21)
------------------------

* The ``watch`` context manager now allows you to either provide
  a callback or do an explicit check afterwards (**warning**: this change
  is not backwards compatible, please update your fabfiles)
* Add support for some network-related operations:
    * get the IPV4 address assigned to an interface
    * get the list of name server IP addresses
* The ``services`` module now supports both upstart and traditional
  SysV-style ``/etc/init.d`` scripts (thanks to Selwin Ong)
* The ``virtualenv`` context manager can now also be used with ``local()``
  (thanks to khorn)
* The ``supervisor`` module now uses ``update`` instead of ``reload``
  to avoid unnecessary restarts (thanks to Dan Fairs)
* Add support for OpenVZ containers (requires a kernel with OpenVZ patches)
* ``pip`` can now use a download cache
* Upgrade Redis version to 2.4.17
* Misc bug fixes and improvements
* Support for Ubuntu 12.04 LTS and Debian 6.0
* Documentation improvements

Version 0.4 (2012-05-30)
------------------------

* Added support for requiring an arbitrary APT source
* Added support for adding APT signing keys
* Added support for requiring a user with a home directory
* Added vagrant helpers
* Fixed Python virtualenv context manager

Version 0.3.2 (2012-03-19)
--------------------------

* Fixed README formatting

Version 0.3.1 (2012-03-19)
--------------------------

* Fixed bug in functional tests runner

Version 0.3 (2012-03-19)
------------------------

* Added support for Shorewall (Shoreline Firewall)
* Fixed Python 2.5 compatibility
* Refactored tests

Version 0.2.1 (2012-03-09)
--------------------------

* Packaging fixes

Version 0.2 (2012-03-09)
------------------------

* Added support for hostname and sysctl (kernel parameters)
* Added support for Redis
* Simplified API for supervisor processes

Version 0.1.1 (2012-02-19)
--------------------------

* Packaging fixes

Version 0.1 (2012-02-19)
------------------------

* Initial release
