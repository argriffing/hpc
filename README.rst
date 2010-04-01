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

Installing python packages
--------------------------

Additional python packages are installed to
the virtual environment ``/brc_share/brc/username/myenv``
which was created using the ``virtualenv.py``
script without truly installing virtualenv.
Because tcsh can not properly run the ``activate`` script,
the virtual environment is done manually.
The package manager pip_ was installed using the command::

    $ /brc_share/brc/username/myenv/bin/easy_install pip

Note that the ``easy_install`` script was created in ``myenv``
as part of an automatic installation of setuptools_
when the virtual environment was created.
Additional python packages and modules such as argparse_
can be installed with pip using commands like this::

    $ /path/to/myenv/bin/pip install -E /path/to/myenv argparse


.. _LSF: http://en.wikipedia.org/wiki/Platform_LSF
.. _tcsh: http://en.wikipedia.org/wiki/Tcsh
.. _pip: http://pip.openplans.org/
.. _argparse: http://code.google.com/p/argparse/
.. _setuptools: http://pypi.python.org/pypi/setuptools
