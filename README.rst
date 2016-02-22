===============================
p4c-bm
===============================

.. image:: https://travis-ci.org/p4lang/p4c-bm.svg?branch=develop
        :target: https://travis-ci.org/p4lang/p4c-bm.svg


Generates the JSON configuration for the `behavioral-model (bmv2)
<https://github.com/p4lang/behavioral-model>`_, as well as the PD (Protocol
Dependent) library C/C++ files, if needed.

Usage
-----

* To install p4c-bm on your machine:

  * :code:`sudo pip install -r requirements.txt`
  * :code:`sudo python setup.py install`


* Using p4c-bm

  * Try :code:`p4c-bmv2 -h`
  * :code:`--json` to generate a JSON representation of the P4 program
  * :code:`--pd` to generate the PD C++ code


* Compiling the PD

  The repository also comes with autotools support. By using it, you can:

  * install the Python p4c-bm code (same as with `setup.py`)
  * compile and (optionally) install the PD fixed libray (`libpdfixed`) and its
    headers. PD fixed is the part of the PD which is not program dependent
    (e.g. multicast interfaces)
  * auto-generate, compile and (optionally) install the PD library (`libpd`) for
    a given P4 program

  If you are just looking to use p4c-bm to generate the JSON input for bmv2, you
  are probably better off not using autotools and simply running :code:`sudo
  python setup.py install`.

  The steps are the following:

  * :code:`./autogen.sh`
  * :code:`./configure`
  * :code:`make`
  * :code:`make install` optionally, as root if needed

  This will compile (and optionally install) the Python code and the PD fixed
  library. If you also want to compile the PD library for a given P4 program,
  you will need to pass the `--with-pd-mk` flag to `configure` and provide the
  `P4_PATH` and `P4_PREFIX` environment variables when calling `make`:

  * :code:`./configure --with-pd-mk`
  * :code:`make 'P4_PATH=<absolute_path_to_p4_program>'
    'P4_PREFIX=<prefix_for_apis>'`

  Because the PD library and PD headers location is independent of the P4
  program you are compiling, generating them for a different P4 program may
  overwrite previous files. You can avoid this by using a different build
  directory for each P4 program (see `automake VPATH builds`__) and by
  installing the compilation products to different locations (e.g. by using the
  `--includedir` and `--libdir` flags for `configure`).

  __ https://www.gnu.org/software/automake/manual/html_node/VPATH-Builds.html

  Of course, you can always manually generate the C++ PD files using `p4c-bmv2`
  and manually copy them to your project directory (and compile them with your
  app).

  If your main project also uses autotools, you may be able to integrate this
  code directly in your infrastructure with :code:`AC_CONFIG_SUBDIRS`


..
   Apache license
   --------------
..
   * Documentation: https://p4c_bm.readthedocs.org.
