check_PROGRAMS = test

test_SOURCES = test.cpp \
thrift_endpoint/src/server.cpp

test_CPPFLAGS = -I$(srcdir)/thrift_endpoint/
test_CPPFLAGS += -I$(top_srcdir)/p4_pd/
test_CPPFLAGS += -I$(top_srcdir)/pdfixed/
# needed for thrift_endpoint
test_CPPFLAGS += -I$(top_srcdir)/thrift_gen/gen-cpp/

test_LDFLAGS = -pthread -lthrift
test_LDADD = $(top_srcdir)/libpdfixed.la $(top_srcdir)/libpd.la

TESTS = ./run_tests.sh
