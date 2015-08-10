ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS} -I m4

SUBDIRS = . tests

standard_thrift_files = \
thrift_gen/gen-cpp/standard_constants.cpp \
thrift_gen/gen-cpp/standard_constants.h \
thrift_gen/gen-cpp/Standard.cpp \
thrift_gen/gen-cpp/Standard.h \
thrift_gen/gen-cpp/standard_types.cpp \
thrift_gen/gen-cpp/standard_types.h

simple_pre_lag_thrift_files = \
thrift_gen/gen-cpp/simple_pre_lag_constants.cpp \
thrift_gen/gen-cpp/simple_pre_lag_constants.h \
thrift_gen/gen-cpp/SimplePreLAG.cpp \
thrift_gen/gen-cpp/SimplePreLAG.h \
thrift_gen/gen-cpp/simple_pre_lag_types.cpp \
thrift_gen/gen-cpp/simple_pre_lag_types.h

thrift_files = \
$(standard_thrift_files) \
$(simple_pre_lag_thrift_files)

standard_IDL = $(top_srcdir)/../submodules/bm/thrift_src/standard.thrift
simple_pre_lag_IDL = $(top_srcdir)/../submodules/bm/thrift_src/simple_pre_lag.thrift

$(thrift_files): $(standard_IDL) $(simple_pre_lag_IDL)
	$(THRIFT) -o $(top_srcdir)/thrift_gen/ --gen cpp -r $(standard_IDL)
	$(THRIFT) -o $(top_srcdir)/thrift_gen/ --gen cpp -r $(simple_pre_lag_IDL)

pd_files = \
p4_pd/src/pd.cpp \
p4_pd/src/pd_learning.cpp \
p4_pd/src/pd_meters.cpp \
p4_pd/src/pd_tables.cpp \
p4_pd/src/pd_ageing.cpp

pd_headers = \
p4_pd/pd/pd.h \
p4_pd/pd/pd_learning.h \
p4_pd/pd/pd_meters.h \
p4_pd/pd/pd_tables.h \
p4_pd/pd/pd_types.h

$(pd_files): $(P4_PATH)
	$(top_srcdir)/../p4c_bm/__main__.py --pd p4_pd/ --p4-prefix $(P4_PREFIX) $(P4_PATH)

BUILT_SOURCES = \
$(thrift_files) \
$(pd_files)

pdf_files = \
pdfixed/src/pd_conn_mgr.cpp \
pdfixed/src/pd_pre.cpp \
pdfixed/src/pd_static.cpp

pdf_headers = \
pdfixed/pd/pd_pre.h \
pdfixed/pd/pd_static.h \
pdfixed/pd/pd_common.h

nobase_include_HEADERS = \
$(pd_headers) \
$(pdf_headers)

lib_LTLIBRARIES = libpd.la libpdfixed.la

libpdfixed_la_SOURCES = \
$(pdf_files)

libpd_la_SOURCES = \
$(BUILT_SOURCES)

AM_CPPFLAGS = -I$(top_srcdir)/pdfixed/
AM_CPPFLAGS += -I$(top_srcdir)/pdfixed/src/
AM_CPPFLAGS += -I$(top_srcdir)/thrift_gen/gen-cpp/
AM_CPPFLAGS += -I$(top_srcdir)/p4_pd/

CLEANFILES = $(BUILT_SOURCES)
