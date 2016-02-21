check_PROGRAMS = test

test_SOURCES = test.cpp \
thrift_endpoint/src/server.cpp

test_CPPFLAGS = -I$(srcdir)/thrift_endpoint/
test_CPPFLAGS += -I$(builddir)/../p4_pd/
test_CPPFLAGS += -I$(top_srcdir)/pdfixed/
# needed for thrift_endpoint
test_CPPFLAGS += -I$(top_builddir)/pdfixed/bmv2_thrift_gen/gen-cpp/

test_LDFLAGS = -pthread -lthrift
test_LDADD = $(top_builddir)/pdfixed/libpdfixed.la $(builddir)/../libpd.la

TESTS = ./run_tests.sh
