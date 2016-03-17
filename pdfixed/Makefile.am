ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS} -I m4

include bmv2_rpc.am

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

pd_conn_mgr_thrift_py = pd_thrift_gen/gen-py/conn_mgr_pd_rpc/constants.py

pd_mc_thrift_py = pd_thrift_gen/gen-py/mc_pd_rpc/constants.py


pd_conn_mgr_IDL = $(srcdir)/thrift/conn_mgr_pd_rpc.thrift
pd_mc_IDL = $(srcdir)/thrift/mc_pd_rpc.thrift
pd_res_IDL = $(srcdir)/thrift/res.thrift

pdfixed_thrift_files = \
$(pd_conn_mgr_thrift_files) \
$(pd_mc_thrift_files) \
$(pd_res_thrift_files) \
$(pd_conn_mgr_thrift_py) \
$(pd_mc_thrift_py)

pdfixed_thrift_files.ts: $(pd_conn_mgr_IDL) $(pd_mc_IDL) $(pd_res_IDL)
	@rm -f pdfixed_thrift_files.tmp
	@touch pdfixed_thrift_files.tmp
	$(THRIFT) -o $(builddir)/pd_thrift_gen/ --gen cpp -r $(pd_conn_mgr_IDL)
	$(THRIFT) -o $(builddir)/pd_thrift_gen/ --gen cpp -r $(pd_mc_IDL)
	$(THRIFT) -o $(builddir)/pd_thrift_gen/ --gen py -r $(pd_conn_mgr_IDL)
	$(THRIFT) -o $(builddir)/pd_thrift_gen/ --gen py -r $(pd_mc_IDL)
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

thrift_py_lzma = $(builddir)/gen-py.tar.lz

$(thrift_py_lzma) : $(pdfixed_thrift_files)
	tar --create -C $(builddir)/pd_thrift_gen/ gen-py/ | lzma > $(thrift_py_lzma)

pdfixedpkgdatadir = $(pkgdatadir)/pdfixed
nobase_pdfixedpkgdata_DATA = $(thrift_py_lzma)

# See http://stackoverflow.com/questions/6395148/install-data-directory-tree-with-massive-number-of-files-using-automake

install-data-hook:
	cd $(DESTDIR)$(pdfixedpkgdatadir); \
	cat $(thrift_py_lzma) | unlzma | tar --list > uninstall_manifest.txt; \
	cat $(thrift_py_lzma) | unlzma | tar --no-same-owner --extract; \
	rm -f $(thrift_py_lzma); \
	cat uninstall_manifest.txt | sed --expression='s/^\|$$/"/g' | xargs chmod a=rX,u+w

uninstall-local:
	cd $(DESTDIR)$(pdfixedpkgdatadir); \
	cat uninstall_manifest.txt | sed --expression='s/ /\\ /g' | xargs rm -f; \
	rm -f uninstall_manifest.txt


BUILT_SOURCES += \
$(pdfixed_thrift_files) \
$(thrift_py_lzma)

pdf_files = \
src/pd_conn_mgr.cpp \
src/pd_notifications.cpp \
src/pd_helpers.cpp \
src/pd_pre.cpp \
src/pd_static.cpp \
src/nn.h

pdf_headers = \
pd/pd_pre.h \
pd/pd_static.h \
pd/pd_common.h

# these are needed when compiling the P4-dependent PD
pdf_int_headers = \
src/pd_conn_mgr.h \
src/pd_helpers.h \
src/pd_notifications.h

pdfixedpkgincludedir = $(pkgincludedir)/pdfixed

nobase_pdfixedpkginclude_HEADERS = \
$(pdf_headers) \
$(pdf_int_headers) \
thrift-src/pdfixed_rpc_server.h \
thrift/res.thrift

# install this script in case it is needed
pdfixedpkgpythondir = $(pkgpythondir)/pdfixed
pdfixedpkgpython_PYTHON = $(top_srcdir)/pd_mk/split_pd_thrift.py

lib_LTLIBRARIES = libbmpdfixed.la libbmpdfixedthrift.la

libbmpdfixed_la_SOURCES = \
$(pdf_files) \
$(thrift_files)

libbmpdfixedthrift_la_SOURCES = \
$(pdfixed_thrift_files) \
thrift-src/pdfixed_rpc_server.cpp

AM_CPPFLAGS = -I$(srcdir)
AM_CPPFLAGS += -I$(srcdir)/src/
AM_CPPFLAGS += -I$(builddir)/pd_thrift_gen/gen-cpp/
AM_CPPFLAGS += -I$(builddir)/bmv2_thrift_gen/gen-cpp/

CLEANFILES += $(BUILT_SOURCES) \
pdfixed_thrift_files.ts
