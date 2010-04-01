Info
====

The hpc is a Red Hat LSF_ system,
and its LSF-related commands include
``bsub``, ``bhist``, ``bjobs``, ``bqueues``, ``bpeek``, and ``bkill``.
The Red Hat version is Enterprise AS release 4 (Nahant Update 5),
and the shell is tcsh_.

Changing shells
---------------

To change from tcsh to bash::

    chsh -s /bin/bash

Note that this could cause problems.
The ``add`` scripts only work with tcsh.
Also, the compute nodes use tcsh.

Installing software from source
-------------------------------

Because I only have enough disk quota in ``/home`` for a few dotfiles,
installed programs such as git and python are prefixed to
``/brc_share/brc/username/install``.

Creating a virtual environment for python packages
--------------------------------------------------

Download virtualenv_ and create a virtual environment::

    $ python virtualenv.py /brc_share/brc/username/myenv

This also installs setuptools_ to the virtual environment,
including the easy_install script which can be used to
install the better package manager pip_.
Note that the ``virtualenv.py`` script can be used without
actually installing virtualenv.

Installing python packages under tcsh
-------------------------------------

The package manager pip_ can be installed using the command::

    $ /brc_share/brc/username/myenv/bin/easy_install pip

Additional python packages and modules such as argparse_
can be installed with pip using commands like this::

    $ /path/to/myenv/bin/pip install -E /path/to/myenv argparse

Installing python packages under bash
-------------------------------------

The bash shell can make use of the ``activate`` and ``deactivate``
commands provided by virtualenv.
Activate a virutal environment as follows::

    $ . /path/to/myenv/bin/activate

Then install pip::

    (myenv)$ easy_install pip

Then install extra python packages::

    (myenv)$ pip install argparse

Leave the virtual python environment
and go back to using the system python environment as follows::

    (myenv)$ deactivate


.. _LSF: http://en.wikipedia.org/wiki/Platform_LSF
.. _tcsh: http://en.wikipedia.org/wiki/Tcsh
.. _pip: http://pip.openplans.org/
.. _argparse: http://code.google.com/p/argparse/
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
