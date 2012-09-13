.. _openvz_module:

:mod:`fabtools.openvz`
----------------------

.. automodule:: fabtools.openvz

    .. seealso:: :ref:`require_openvz_module`

    Manage templates
    ~~~~~~~~~~~~~~~~

    .. autofunction:: download_template

    Manage containers
    ~~~~~~~~~~~~~~~~~

    .. autofunction:: exists
    .. autofunction:: create
    .. autofunction:: set
    .. autofunction:: status
    .. autofunction:: start
    .. autofunction:: stop
    .. autofunction:: restart
    .. autofunction:: destroy


    Run commands inside a container
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. autofunction:: exec2
    .. autofunction:: guest

    Container class
    ~~~~~~~~~~~~~~~

    .. autoclass:: fabtools.openvz.container.Container
        :members:
