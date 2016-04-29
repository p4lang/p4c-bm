===============================
p4c-bm
===============================

.. image:: https://travis-ci.org/p4lang/p4c-bm.svg?branch=develop
        :target: https://travis-ci.org/p4lang/p4c-bm.svg


Generates the JSON configuration for the `behavioral-model (bmv2)
<https://github.com/p4lang/behavioral-model>`_.

Important: the PD has been moved out of this repository and split between the
`bmv2 repository <https://github.com/p4lang/behavioral-model>`_ (for fixed part
of the PD) and the new `p4-build repository
<https://github.com/p4lang/p4-build>`_ (build infrastructure for the
auto-generated / program-dependent part of the PD).

Usage
-----

* To install p4c-bm on your machine:

  * :code:`sudo pip install -r requirements.txt`
  * :code:`sudo pip install -r requirements_v1_1.txt` if you are interested in
    compiling P4 v1.1 programs
  * :code:`sudo python setup.py install`


* Using p4c-bm

  * Try :code:`p4c-bmv2 -h`
  * :code:`--json` to generate a JSON representation of the P4 program
  * :code:`--pd` to generate the PD C++ code
  * :code:`--p4-v1.1` if your input program is a P4 v1.1 program


* To install in a non-default location, you can use:

  * :code:`python setup.py build install --prefix <your_path>
    [--single-version-externally-managed] --record install_files.txt`
  * :code:`cat install_files.txt | xargs rm -rf` if you need to uninstall later
    on

..
   Apache license
   --------------
..
   * Documentation: https://p4c_bm.readthedocs.org.
