#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([p4c_bm], [0.1], [])
AM_INIT_AUTOMAKE([foreign subdir-objects])
# This prevents autotools from automatically adding -O2 flag.
: ${CXXFLAGS=""}
dnl AC_CONFIG_SRCDIR([pdfixed/thrift-src/pdfixed_rpc_server.h])
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])

AM_PATH_PYTHON([2.7],,)
LT_INIT

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC
AC_PROG_CPP
AC_PROG_INSTALL
AC_PROG_MAKE_SET

# Checks for libraries.

# Add picky flags
PICKY_CXXFLAGS="-Wall -Werror -Wextra"
PICKY_CFLAGS=""
AC_SUBST([PICKY_CXXFLAGS])
AC_SUBST([PICKY_CFLAGS])
AC_SUBST([DEBUG_CPPFLAGS])

# Checks for header files.
AC_LANG_PUSH(C)
AC_LANG_PUSH(C++)

# Check for thrift support (Facebook's Thrift RPC library)
AC_PATH_PROG([THRIFT], [thrift], [])
AS_IF([test x"$THRIFT" = x],
[AC_MSG_ERROR([cannot find thrift])])

# Check for libjudy, libnanomsg
AC_CHECK_LIB([Judy], [Judy1Next], [], [AC_MSG_ERROR([Missing libJudy])])
AC_CHECK_LIB([nanomsg], [nn_errno], [], [AC_MSG_ERROR([Missing libnanomsg])])
AC_CHECK_LIB([pthread], pthread_create, [], [AC_MSG_ERROR([required library pthread missing])])

# Checks for typedefs, structures, and compiler characteristics.
# introduces in autoconf 2.69
# AC_CHECK_HEADER_STDBOOL
AC_TYPE_SIZE_T
AC_TYPE_UINT64_T
AC_LANG_POP(C++)

# Generate makefiles
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
