ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS} -I m4

pd_conn_mgr_IDL = $(srcdir)/pdfixed/thrift/conn_mgr_pd_rpc.thrift
pd_mc_IDL = $(srcdir)/pdfixed/thrift/mc_pd_rpc.thrift
pd_res_IDL = $(srcdir)/pdfixed/thrift/res.thrift

pd_conn_mgr_thrift_files = \
pd_thrift_gen/gen-cpp/conn_mgr.cpp \
pd_thrift_gen/gen-cpp/conn_mgr.h \
pd_thrift_gen/gen-cpp/conn_mgr_pd_rpc_constants.cpp \
pd_thrift_gen/gen-cpp/conn_mgr_pd_rpc_constants.h \
pd_thrift_gen/gen-cpp/conn_mgr_pd_rpc_types.cpp \
pd_thrift_gen/gen-cpp/conn_mgr_pd_rpc_types.h

pd_mc_thrift_files = \
pd_thrift_gen/gen-cpp/mc.cpp \
pd_thrift_gen/gen-cpp/mc.h \
pd_thrift_gen/gen-cpp/mc_pd_rpc_constants.cpp \
pd_thrift_gen/gen-cpp/mc_pd_rpc_constants.h \
pd_thrift_gen/gen-cpp/mc_pd_rpc_types.cpp \
pd_thrift_gen/gen-cpp/mc_pd_rpc_types.h

pd_res_thrift_files = \
pd_thrift_gen/gen-cpp/res_constants.cpp \
pd_thrift_gen/gen-cpp/res_constants.h \
pd_thrift_gen/gen-cpp/res_types.cpp \
pd_thrift_gen/gen-cpp/res_types.h

pdfixed_thrift_files = \
$(pd_conn_mgr_thrift_files) \
$(pd_mc_thrift_files) \
$(pd_res_thrift_files) \
$(pd_conn_mgr_thrift_py) \
$(pd_mc_thrift_py)

pdfixed_thrift_files.ts: $(pd_conn_mgr_IDL) $(pd_mc_IDL) $(pd_res_IDL)
	@mkdir -p $(srcdir)/pd_thrift_gen
	@rm -f pdfixed_thrift_files.tmp
	@touch pdfixed_thrift_files.tmp
	$(THRIFT) -o $(srcdir)/pd_thrift_gen/ --gen cpp -r $(pd_conn_mgr_IDL)
	$(THRIFT) -o $(srcdir)/pd_thrift_gen/ --gen cpp -r $(pd_mc_IDL)
	$(THRIFT) -o $(srcdir)/pd_thrift_gen/ --gen py -r $(pd_conn_mgr_IDL)
	$(THRIFT) -o $(srcdir)/pd_thrift_gen/ --gen py -r $(pd_mc_IDL)
	@mv -f pdfixed_thrift_files.tmp $@

$(pdfixed_thrift_files): pdfixed_thrift_files.ts
## Recover from the removal of $@
	@if test -f $@; then :; else \
	  trap 'rm -rf pdfixed_thrift_files.lock pdfixed_thrift_files.ts' 1 2 13 15; \
## mkdir is a portable test-and-set
	if mkdir pdfixed_thrift_files.lock 2>/dev/null; then \
## This code is being executed by the first process.
	  rm -f pdfixed_thrift_files.ts; \
	  $(MAKE) $(AM_MAKEFLAGS) pdfixed_thrift_files.ts; \
	  result=$$?; rm -rf pdfixed_thrift_files.lock; exit $$result; \
	else \
## This code is being executed by the follower processes.
## Wait until the first process is done.
	  while test -d pdfixed_thrift_files.lock; do sleep 1; done; \
## Succeed if and only if the first process succeeded.
	    test -f pdfixed_thrift_files.ts; \
	  fi; \
	fi

$(pdf_files) : pdfixed_thrift_files.ts

pdf_files = \
pdfixed/src/pd_conn_mgr.cpp \
pdfixed/src/pd_pre.cpp \
pdfixed/src/pd_notifications.cpp \
pdfixed/src/pd_static.cpp

pdf_headers = \
pdfixed/pd/pd_pre.h \
pdfixed/pd/pd_static.h \
pdfixed/pd/pd_common.h

more_pdf_headers = \
pdfixed/src/pd_conn_mgr.h \
pdfixed/src/pd_notifications.h \
pdfixed/src/nn.h

pkglib_LTLIBRARIES = libpdfixed.la libpdfixedthrift.la

nobase_pkginclude_HEADERS = \
$(pdf_headers) \
$(more_pdf_headers)

libpdfixed_la_SOURCES = \
$(pdf_files)

BMV2_INC_DIR = $(includedir)/bm_sim
libpdfixed_la_CXXFLAGS = -I $(BMV2_INC_DIR) -std=c++11

libpdfixedthrift_la_SOURCES = \
$(pdfixed_thrift_files) \
pdfixed/thrift-src/pdfixed_rpc_server.cpp

libpdfixedthrift_la_CXXFLAGS = -I $(BMV2_INC_DIR) -std=c++11

AM_CPPFLAGS = -I$(srcdir)/pdfixed/
AM_CPPFLAGS += -I$(srcdir)/pdfixed/src/
AM_CPPFLAGS += -I$(srcdir)/pd_thrift_gen/gen-cpp/

all-local: pdfixed_thrift_files.ts $(pkglib_LTLIBRARIES) $(nobase_pkginclude_HEADERS)

# setup.py needs sudo permissions if files are installed to /usr/local.. 
# use of DESTDIR is running into problems with PYTHONPATH (TBD)
# install-exec-local: all-local
# 	$(PYTHON) $(srcdir)/setup.py install --prefix $(DESTDIR)

CLEANFILES = \
pdfixed_thrift_files.ts $(pdfixed_thrift_files) \
pd_thrift_gen/gen_cpp/*
