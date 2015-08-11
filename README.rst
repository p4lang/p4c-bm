===============================
p4c-bm
===============================

.. image:: https://travis-ci.org/p4lang/behavioral-model.svg?branch=develop
        :target: https://travis-ci.org/p4lang/behavioral-model.svg


Generates the JSON configuration for the behavioral-model, as well as the PD C++ files if needed

Usage
-----

* To install p4c-bm on your machine

  1. sudo pip install -r requirements.txt
  2. sudo python setup.py install


* Using p4c-bm

  * Try p4c-bm -h
  * --json to generate a JSON representation of the P4 program
  * --pd to generate the PD C++ code


* Compiling the PD

  You can copy the generated C++ PD file to your project directory (and compile
  them with your app).

  You can also use the pd_mk directory to compile the PD code:

    0. cd to pd_mk
    1. ./configure 'P4_PATH=\ *path_to_p4_program*\ ' 'P4_PREFIX=\ *prefix_for_apis*\ ' --includedir=\ *target_dir_for_headers* --libdir=\ *target_dir_for_libraries*
    2. make
    3. make install

  You will find the PD headers (fixed and generated) in *target_dir_for_headers*
  and the libraries (libpdfixed and libpd) in *target_dir_for_libraries*.

  If your main project also uses autotools, you may be able to integrate pd_mk
  directly in your infrastructure with **AC_CONFIG_SUBDIRS**


Apache license
--------------
..
   * Documentation: https://p4c_bm.readthedocs.org.
