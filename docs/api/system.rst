.. _system_module:

:mod:`fabtools.system`
----------------------

.. automodule:: fabtools.system

    OS detection
    ~~~~~~~~~~~~

    .. autofunction:: distrib_id
    .. autofunction:: distrib_family
    .. autofunction:: distrib_release
    .. autofunction:: distrib_codename
    .. autofunction:: distrib_desc

    Hardware detection
    ~~~~~~~~~~~~~~~~~~

    .. autofunction:: get_arch
    .. autofunction:: cpus

    Hostname
    ~~~~~~~~

    .. autofunction:: get_hostname
    .. autofunction:: set_hostname

    Kernel parameters
    ~~~~~~~~~~~~~~~~~

    .. autofunction:: get_sysctl
    .. autofunction:: set_sysctl

    Locales
    ~~~~~~~

    .. autofunction:: supported_locales

    Time
    ~~~~~~~

    .. autofunction:: time
