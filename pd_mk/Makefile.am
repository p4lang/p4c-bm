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

simple_switch_thrift_files = \
thrift_gen/gen-cpp/simple_switch_constants.cpp \
thrift_gen/gen-cpp/simple_switch_constants.h \
thrift_gen/gen-cpp/SimpleSwitch.cpp \
thrift_gen/gen-cpp/SimpleSwitch.h \
thrift_gen/gen-cpp/simple_switch_types.cpp \
thrift_gen/gen-cpp/simple_switch_types.h

thrift_files = \
$(standard_thrift_files) \
$(simple_pre_lag_thrift_files) \
$(simple_switch_thrift_files)

standard_IDL = $(top_srcdir)/../submodules/bm/thrift_src/standard.thrift
simple_pre_lag_IDL = $(top_srcdir)/../submodules/bm/thrift_src/simple_pre_lag.thrift
simple_switch_IDL = $(top_srcdir)/../submodules/bm/targets/simple_switch/thrift/simple_switch.thrift

template_cpp_files = \
$(top_srcdir)/../p4c_bm/templates/src/pd.cpp \
$(top_srcdir)/../p4c_bm/templates/src/pd_learning.cpp \
$(top_srcdir)/../p4c_bm/templates/src/pd_meters.cpp \
$(top_srcdir)/../p4c_bm/templates/src/pd_counters.cpp \
$(top_srcdir)/../p4c_bm/templates/src/pd_tables.cpp \
$(top_srcdir)/../p4c_bm/templates/src/pd_ageing.cpp \
$(top_srcdir)/../p4c_bm/templates/src/pd_mirroring.cpp

template_h_files = \
$(top_srcdir)/../p4c_bm/templates/pd/pd.h \
$(top_srcdir)/../p4c_bm/templates/pd/pd_learning.h \
$(top_srcdir)/../p4c_bm/templates/pd/pd_meters.h \
$(top_srcdir)/../p4c_bm/templates/pd/pd_counters.h \
$(top_srcdir)/../p4c_bm/templates/pd/pd_tables.h \
$(top_srcdir)/../p4c_bm/templates/pd/pd_types.h \
$(top_srcdir)/../p4c_bm/templates/pd/pd_mirroring.h

template_thrift_files = \
$(top_srcdir)/../p4c_bm/templates/thrift/p4_pd_rpc.thrift \
$(top_srcdir)/../p4c_bm/templates/thrift-src/p4_pd_rpc_server.ipp \
$(top_srcdir)/../p4c_bm/templates/thrift-src/pd_rpc_server.cpp

template_files = \
$(template_cpp_files) \
$(template_h_files) \
$(template_thrift_files)


# See http://www.gnu.org/software/automake/manual/html_node/Multiple-Outputs.html
thrift_files.ts: $(standard_IDL) $(simple_pre_lag_IDL)
	@rm -f thrift_files.tmp
	@touch thrift_files.tmp
	$(THRIFT) -o $(top_srcdir)/thrift_gen/ --gen cpp -r $(standard_IDL)
	$(THRIFT) -o $(top_srcdir)/thrift_gen/ --gen cpp -r $(simple_pre_lag_IDL)
	$(THRIFT) -o $(top_srcdir)/thrift_gen/ --gen cpp -r $(simple_switch_IDL)
	@mv -f thrift_files.tmp $@
$(thrift_files): thrift_files.ts
## Recover from the removal of $@
	@if test -f $@; then :; else \
	  trap 'rm -rf thrift_files.lock thrift_files.ts' 1 2 13 15; \
## mkdir is a portable test-and-set
	if mkdir thrift_files.lock 2>/dev/null; then \
## This code is being executed by the first process.
	  rm -f thrift_files.ts; \
	  $(MAKE) $(AM_MAKEFLAGS) thrift_files.ts; \
	  result=$$?; rm -rf thrift_files.lock; exit $$result; \
	else \
## This code is being executed by the follower processes.
## Wait until the first process is done.
	  while test -d thrift_files.lock; do sleep 1; done; \
## Succeed if and only if the first process succeeded.
	    test -f thrift_files.ts; \
	  fi; \
	fi

pd_files = \
p4_pd/src/pd.cpp \
p4_pd/src/pd_learning.cpp \
p4_pd/src/pd_meters.cpp \
p4_pd/src/pd_counters.cpp \
p4_pd/src/pd_tables.cpp \
p4_pd/src/pd_ageing.cpp \
p4_pd/src/pd_mirroring.cpp

pd_headers = \
p4_pd/pd/pd.h \
p4_pd/pd/pd_learning.h \
p4_pd/pd/pd_meters.h \
p4_pd/pd/pd_counters.h \
p4_pd/pd/pd_tables.h \
p4_pd/pd/pd_types.h \
p4_pd/pd/pd_mirroring.h

pd_p4_IDL = p4_pd/thrift/p4_pd_rpc.thrift
pd_p4_src = \
p4_pd/thrift-src/p4_pd_rpc_server.ipp \
p4_pd/thrift-src/pd_rpc_server.cpp \
p4_pd/thrift-src/pd_rpc_server.h

pd_files-sanitize :
	@echo "$(P4_PATH)" > .bmv2-pd-sane.tmp
	@echo "$(P4_PREFIX)" >> .bmv2-pd-sane.tmp
	@if test -f .bmv2-pd-sane; then :; else \
		touch .bmv2-pd-sane;\
	fi
	@if diff .bmv2-pd-sane .bmv2-pd-sane.tmp >/dev/null; then :; else \
		echo "p4c-bm env change"; \
		$(MAKE) clean; \
	fi
	@mv .bmv2-pd-sane.tmp .bmv2-pd-sane

.PHONY : pd_files-sanitize

pd_files.ts : $(P4_PATH) $(template_files) | pd_files-sanitize
	@rm -f pd_files.tmp
	@touch pd_files.tmp
	$(top_srcdir)/../p4c_bm/__main__.py --pd p4_pd/ --p4-prefix $(P4_PREFIX) $(P4_PATH)
	@mv -f pd_files.tmp $@
$(pd_files) $(pd_p4_IDL) $(pd_p4_src) : pd_files.ts
## Recover from the removal of $@
	@if test -f $@; then :; else \
	  trap 'rm -rf pd_files.lock pd_files.ts' 1 2 13 15; \
## mkdir is a portable test-and-set
	if mkdir pd_files.lock 2>/dev/null; then \
## This code is being executed by the first process.
	  rm -f pd_files.ts; \
	  $(MAKE) $(AM_MAKEFLAGS) pd_files.ts; \
	  result=$$?; rm -rf pd_files.lock; exit $$result; \
	else \
## This code is being executed by the follower processes.
## Wait until the first process is done.
	  while test -d pd_files.lock; do sleep 1; done; \
## Succeed if and only if the first process succeeded.
	    test -f pd_files.ts; \
	  fi; \
	fi

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


pd_conn_mgr_IDL = $(top_srcdir)/../pdfixed/thrift/conn_mgr_pd_rpc.thrift
pd_mc_IDL = $(top_srcdir)/../pdfixed/thrift/mc_pd_rpc.thrift
pd_res_IDL = $(top_srcdir)/../pdfixed/thrift/res.thrift

pdfixed_thrift_files = \
$(pd_conn_mgr_thrift_files) \
$(pd_mc_thrift_files) \
$(pd_res_thrift_files) \
$(pd_conn_mgr_thrift_py) \
$(pd_mc_thrift_py)

pdfixed_thrift_files.ts: $(pd_conn_mgr_IDL) $(pd_mc_IDL) $(pd_res_IDL)
	@rm -f pdfixed_thrift_files.tmp
	@touch pdfixed_thrift_files.tmp
	$(THRIFT) -o $(top_srcdir)/pd_thrift_gen/ --gen cpp -r $(pd_conn_mgr_IDL)
	$(THRIFT) -o $(top_srcdir)/pd_thrift_gen/ --gen cpp -r $(pd_mc_IDL)
	$(THRIFT) -o $(top_srcdir)/pd_thrift_gen/ --gen py -r $(pd_conn_mgr_IDL)
	$(THRIFT) -o $(top_srcdir)/pd_thrift_gen/ --gen py -r $(pd_mc_IDL)
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

pd_p4_thrift_files = \
pd_thrift_gen/gen-cpp/p4_prefix0.cpp \
pd_thrift_gen/gen-cpp/p4_prefix1.cpp \
pd_thrift_gen/gen-cpp/p4_prefix2.cpp \
pd_thrift_gen/gen-cpp/p4_prefix.h \
pd_thrift_gen/gen-cpp/p4_pd_rpc_constants.cpp \
pd_thrift_gen/gen-cpp/p4_pd_rpc_constants.h \
pd_thrift_gen/gen-cpp/p4_pd_rpc_types.cpp \
pd_thrift_gen/gen-cpp/p4_pd_rpc_types.h

pd_thrift_files = $(pd_p4_thrift_files)

pd_p4_py = pd_thrift_gen/gen-py/p4_pd_rpc/constants.py

pd_thrift_files.ts: $(pd_files) $(pd_p4_IDL) $(pd_res_IDL)
	@rm -f pd_thrift_files.tmp
	@touch pd_thrift_files.tmp
	$(THRIFT) -o $(top_srcdir)/pd_thrift_gen/ -I $(top_srcdir)/../pdfixed/thrift/ --gen cpp -r $(pd_p4_IDL)
	$(THRIFT) -o $(top_srcdir)/pd_thrift_gen/ -I $(top_srcdir)/../pdfixed/thrift/ --gen py -r $(pd_p4_IDL)
	mv -f pd_thrift_gen/gen-cpp/$(P4_PREFIX).h pd_thrift_gen/gen-cpp/p4_prefix.h
	sed --in-place 's/include "$(P4_PREFIX).h"/include "p4_prefix.h"/' pd_thrift_gen/gen-cpp/$(P4_PREFIX).cpp
	python $(top_srcdir)/split_pd_thrift.py pd_thrift_gen/gen-cpp/$(P4_PREFIX).cpp pd_thrift_gen/gen-cpp/ 3
	@mv -f pd_thrift_files.tmp $@
$(pd_thrift_files): pd_thrift_files.ts
## Recover from the removal of $@
	@if test -f $@; then :; else \
	  trap 'rm -rf pd_thrift_files.lock pd_thrift_files.ts' 1 2 13 15; \
## mkdir is a portable test-and-set
	if mkdir pd_thrift_files.lock 2>/dev/null; then \
## This code is being executed by the first process.
	  rm -f pd_thrift_files.ts; \
	  $(MAKE) $(AM_MAKEFLAGS) pd_thrift_files.ts; \
	  result=$$?; rm -rf pd_thrift_files.lock; exit $$result; \
	else \
## This code is being executed by the follower processes.
## Wait until the first process is done.
	  while test -d pd_thrift_files.lock; do sleep 1; done; \
## Succeed if and only if the first process succeeded.
	    test -f pd_thrift_files.ts; \
	  fi; \
	fi

thrift_py_lzma = gen-py.tar.lz

$(thrift_py_lzma) : $(pdfixed_thrift_files) $(pd_thrift_files)
	tar --create -C pd_thrift_gen/ gen-py/ | lzma > $(thrift_py_lzma)

nobase_data_DATA = $(thrift_py_lzma)

# See http://stackoverflow.com/questions/6395148/install-data-directory-tree-with-massive-number-of-files-using-automake

install-data-hook:
	cd $(DESTDIR)$(datadir); \
	cat $(thrift_py_lzma) | unlzma | tar --list > uninstall_manifest.txt; \
	cat $(thrift_py_lzma) | unlzma | tar --no-same-owner --extract; \
	rm -f $(thrift_py_lzma); \
	cat uninstall_manifest.txt | sed --expression='s/^\|$$/"/g' | xargs chmod a=rX,u+w

uninstall-local:
	cd $(DESTDIR)$(datadir); \
	cat uninstall_manifest.txt | sed --expression='s/ /\\ /g' | xargs rm -f; \
	rm -f uninstall_manifest.txt


BUILT_SOURCES = \
$(thrift_files) \
$(pd_files) \
$(pdfixed_thrift_files) \
$(pd_thrift_files) \
$(thrift_py_lzma)

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
$(pdf_headers) \
pdfixed/thrift-src/pdfixed_rpc_server.h \
p4_pd/thrift-src/pd_rpc_server.h

lib_LTLIBRARIES = libpd.la libpdfixed.la libpdfixedthrift.la libpdthrift.la

libpdfixed_la_SOURCES = \
$(pdf_files)

libpd_la_SOURCES = \
$(thrift_files) \
$(pd_files)

libpdfixedthrift_la_SOURCES = \
$(pdfixed_thrift_files) \
pdfixed/thrift-src/pdfixed_rpc_server.cpp

libpdthrift_la_SOURCES = \
$(pd_thrift_files) \
p4_pd/thrift-src/pd_rpc_server.cpp

AM_CPPFLAGS = -I$(top_srcdir)/pdfixed/
AM_CPPFLAGS += -I$(top_srcdir)/pdfixed/src/
AM_CPPFLAGS += -I$(top_srcdir)/thrift_gen/gen-cpp/
AM_CPPFLAGS += -I$(top_srcdir)/p4_pd/
AM_CPPFLAGS += -I$(top_srcdir)/pd_thrift_gen/gen-cpp/

CLEANFILES = $(BUILT_SOURCES) \
thrift_files.ts pd_files.ts pdfixed_thrift_files.ts pd_thrift_files.ts \
.bmv2-pd-sane

# this causes 'make clean' to fail when run several times
# clean-local:
# 	rm -rf pd_thrift_gen thrift_gen
