#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.68])
AC_INIT([p4c_bm], [0.1], [antonin@barefootnetworks.com])
# This prevents autotools from automatically adding -O2 flag.
: ${CXXFLAGS=""}
AM_INIT_AUTOMAKE([-Wportability -Werror foreign subdir-objects])

AC_CONFIG_HEADERS([config.h])

AC_CONFIG_MACRO_DIR([m4])

# will abort if there is no Python interpreter >= 2.7
AM_PATH_PYTHON([2.7])

AC_ARG_WITH([pd-mk],
    AS_HELP_STRING([--with-pd-mk],
                   [Include pd_mk sub-directory when building,
                    make sure that the P4_PATH and P4_PREFIX env variable
                    are defined when you run make]),
    [want_pd_mk=yes], [])

AM_CONDITIONAL([COND_PD_MK], [test "$want_pd_mk" = yes])

# Enable Openflow
AC_WITH([of], [want_of=yes], [])
AM_CONDITIONAL([COND_PLUGIN_OPENFLOW], [test "$want_of" = yes])

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC
LT_INIT

# enforce -std=c++11
AX_CXX_COMPILE_STDCXX_11([noext],[mandatory])

# Checks for header files.
AC_LANG_PUSH(C)
AC_LANG_PUSH(C++)

AC_CHECK_HEADERS([algorithm array cassert cmath queue \
cstdio string sys/stat.h sys/types.h ctime tuple unistd.h unordered_map \
utility vector], [], [AC_MSG_ERROR([Missing header file])])

# Check for thrift binary
AC_PATH_PROG([THRIFT], [thrift], [])
AS_IF([test x"$THRIFT" = x],
[AC_MSG_ERROR([cannot find thrift])])

# Check for libjudy, libnanomsg, pthread
AC_CHECK_LIB([Judy], [Judy1Next], [], [AC_MSG_ERROR([Missing libJudy])])
AC_CHECK_LIB([nanomsg], [nn_errno], [], [AC_MSG_ERROR([Missing libnanomsg])])
AC_CHECK_LIB([pthread], pthread_create, [], [AC_MSG_ERROR([required library pthread missing])])

# C++ libraries are harder (http://nerdland.net/2009/07/detecting-c-libraries-with-autotools/),
# so use headers to check
AC_CHECK_HEADER([thrift/Thrift.h], [], [AC_MSG_ERROR([Thrift headers not found. Install Thrift from http://thrift.apache.org/docs/install/])])

# Checks for typedefs, structures, and compiler characteristics.
# introduced in autoconf 2.69
# AC_CHECK_HEADER_STDBOOL
AC_TYPE_SIZE_T
AC_TYPE_UINT64_T
AC_LANG_POP(C++)

AC_PROG_SED
AC_CHECK_PROG([tar], [tar], [tar])

# Generate makefiles
AC_CONFIG_FILES([Makefile
                 pdfixed/Makefile
                 pd_mk/Makefile
                 pd_mk/tests/Makefile])

AC_OUTPUT
