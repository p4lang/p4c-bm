#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.68])
AC_INIT([pd_tests], [0.1], [antonin@barefootnetworks.com])
# This prevents autotools from automatically adding -O2 flag.
: ${CXXFLAGS=""}
AM_INIT_AUTOMAKE([foreign subdir-objects])
dnl AC_CONFIG_SRCDIR([modules/bm_sim/src/checksums.cpp])
AC_CONFIG_HEADERS([config.h])

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC
LT_INIT

AC_CONFIG_MACRO_DIR([m4])

# enforce -std=c++11
AX_CXX_COMPILE_STDCXX_11([noext],[mandatory])

# Add picky flags
PICKY_CXXFLAGS="-Wall -Werror -Wextra"
PICKY_CFLAGS=""
AC_SUBST([PICKY_CXXFLAGS])
AC_SUBST([PICKY_CFLAGS])
AC_SUBST([DEBUG_CPPFLAGS])

# That was a bad idea I think: you don't want to have to run ./configure
# everytime you swith P4 programs, it is flaky. Instead I just use environment
# variables in Makefile.am. I'm keeping this here in case I change my mind.

# AC_ARG_VAR([P4_PATH],[P4 Program for which you want to generate the PD])
# AC_ARG_VAR([P4_PREFIX],[Prefix to use for the PD APIs])

# AM_CONDITIONAL([P4_PATH_SET], [test ! -z "$P4_PATH"])
# AM_COND_IF([P4_PATH_SET], [], [AC_MSG_ERROR([P4_PATH not defined!])])

# AM_CONDITIONAL([P4_PREFIX_SET], [test ! -z "$P4_PREFIX"])
# AM_COND_IF([P4_PREFIX_SET], [], [AC_MSG_ERROR([P4_PREFIX not defined!])])

# Checks for header files.
AC_LANG_PUSH(C)
AC_LANG_PUSH(C++)

AC_CHECK_HEADERS([algorithm array cassert cmath queue \
cstdio string sys/stat.h sys/types.h ctime tuple unistd.h unordered_map \
utility vector], [], [AC_MSG_ERROR([Missing header file])])

# Check for thrift support (Facebook's Thrift RPC library)
AC_PATH_PROG([THRIFT], [thrift], [])
AS_IF([test x"$THRIFT" = x],
[AC_MSG_ERROR([cannot find thrift])])

# Check for libjudy, libnanomsg
AC_CHECK_LIB([Judy], [Judy1Next], [], [AC_MSG_ERROR([Missing libJudy])])
AC_CHECK_LIB([nanomsg], [nn_errno], [], [AC_MSG_ERROR([Missing libnanomsg])])
AC_CHECK_LIB([pthread], pthread_create, [], [AC_MSG_ERROR([required library pthread missing])])

# C++ libraries are harder (http://nerdland.net/2009/07/detecting-c-libraries-with-autotools/),
# so use headers to check
AC_CHECK_HEADER([thrift/Thrift.h], [], [AC_MSG_ERROR([Thrift headers not found. Install Thrift from http://thrift.apache.org/docs/install/])])

# Checks for typedefs, structures, and compiler characteristics.
# introduces in autoconf 2.69
# AC_CHECK_HEADER_STDBOOL
AC_TYPE_SIZE_T
AC_TYPE_UINT64_T
AC_LANG_POP(C++)

# Generate makefiles
AC_CONFIG_FILES([Makefile
	         tests/Makefile])
AC_OUTPUT
