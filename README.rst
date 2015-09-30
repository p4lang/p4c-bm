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

  You can copy the generated C++ PD file to your project directory (and compile
  them with your app).

  You can also use the pd_mk directory to compile the PD code:

  * :code:`cd pd_mk/`
  * :code:`./configure --includedir=<target_dir_for_headers> --libdir=<target_dir_for_libraries>`
  * :code:`make 'P4_PATH=<path_to_p4_program>' 'P4_PREFIX=<prefix_for_apis>'`
  * :code:`make install`

  You will find the PD headers (fixed and generated) in *target_dir_for_headers*
  and the libraries (libpdfixed and libpd) in *target_dir_for_libraries*.

  If your main project also uses autotools, you may be able to integrate pd_mk
  directly in your infrastructure with :code:`AC_CONFIG_SUBDIRS`


..
   Apache license
   --------------
..
   * Documentation: https://p4c_bm.readthedocs.org.
