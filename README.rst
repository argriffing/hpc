Info
====

The hpc is a Red Hat LSF_ system,
and its LSF-related commands include
``bsub``, ``bhist``, ``bjobs``, ``bqueues``, ``bpeek``, and ``bkill``.
The Red Hat version is Enterprise AS release 4 (Nahant Update 5),
and the shell is tcsh_.
More info about the cluster is here:
http://www.ncsu.edu/itd/hpc/Documents/BladeCenter/GettingStartedbc.php

Basic LSF commands (this webpage is for a different cluster):
http://kipac-prod.stanford.edu/collab/computing/docs/lsfbasics

Changing shells
---------------

To change from tcsh to bash::

    chsh -s /bin/bash

Note that this could cause problems:

- The ``add`` scripts only work with tcsh.
- The tcsh shell is already configured with a bunch of paths
  and environment variables required for LSF.

The shell change does not take effect until you log out and back in again.
Furthermore, if you log in to the generic login address and it sends
you to a different login node, then you will need to chsh again and re-login.

Startup files
-------------

This web page has some information about which startup file
is sourced at which time for each shell.
http://hayne.net/MacDev/Notes/unixFAQ.html#loginShell

I think that the same startup files are used regardless
of the specific login node,
unlike the node-specific conditions encountered for chsh.

Using ``screen``
----------------

If you want to leave a terminal open while you work on something else,
or if you want to leave a terminal open so that you can work on it from
a different login, then gnu screen_ is useful.
It has been enhanced for Ubuntu as byobu_ and can be installed
on the hpc by extracting http://people.ubuntu.com/~kirkland/byobu/byobu.tar.gz
to your home directory.

Using ``bsub``
--------------

The program called bsub is the primary way to access
the resources of an LSF cluster.
The example bsub script can be run as follows::

    $ bsub < hello.bsub

Installing software from source
-------------------------------

Because I only have enough disk quota in ``/home`` for a few dotfiles_,
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
Activate a virtual environment as follows::

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
.. _byobu: https://launchpad.net/byobu
.. _screen: http://en.wikipedia.org/wiki/GNU_Screen
.. _dotfiles: http://en.wikipedia.org/wiki/Dot_file
