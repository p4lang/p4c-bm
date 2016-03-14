ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS} -I m4

SUBDIRS = . tests

template_cpp_files = \
$(top_srcdir)/p4c_bm/templates/src/pd.cpp \
$(top_srcdir)/p4c_bm/templates/src/pd_learning.cpp \
$(top_srcdir)/p4c_bm/templates/src/pd_meters.cpp \
$(top_srcdir)/p4c_bm/templates/src/pd_counters.cpp \
$(top_srcdir)/p4c_bm/templates/src/pd_tables.cpp \
$(top_srcdir)/p4c_bm/templates/src/pd_ageing.cpp \
$(top_srcdir)/p4c_bm/templates/src/pd_mirroring.cpp

template_h_files = \
$(top_srcdir)/p4c_bm/templates/pd/pd.h \
$(top_srcdir)/p4c_bm/templates/pd/pd_learning.h \
$(top_srcdir)/p4c_bm/templates/pd/pd_meters.h \
$(top_srcdir)/p4c_bm/templates/pd/pd_counters.h \
$(top_srcdir)/p4c_bm/templates/pd/pd_tables.h \
$(top_srcdir)/p4c_bm/templates/pd/pd_types.h \
$(top_srcdir)/p4c_bm/templates/pd/pd_mirroring.h

template_thrift_files = \
$(top_srcdir)/p4c_bm/templates/thrift/p4_pd_rpc.thrift \
$(top_srcdir)/p4c_bm/templates/thrift-src/p4_pd_rpc_server.ipp \
$(top_srcdir)/p4c_bm/templates/thrift-src/pd_rpc_server.cpp

template_plugin_files =

template_files = \
$(template_cpp_files) \
$(template_h_files) \
$(template_thrift_files) \
$(template_plugin_files)

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

plugin_files =
plugin_headers =

pd_p4_IDL = p4_pd/thrift/p4_pd_rpc.thrift
pd_p4_src = \
$(builddir)/p4_pd/thrift-src/p4_pd_rpc_server.ipp \
$(builddir)/p4_pd/thrift-src/pd_rpc_server.cpp \
$(builddir)/p4_pd/thrift-src/pd_rpc_server.h

# automake does not report it as non-portable
P4_PREFIX ?= test
P4_PATH ?= $(top_srcdir)/pd_mk/tests/test.p4
P4_OPTIONS ?=

pd_files-sanitize :
	@echo "$(P4_PATH)" > .bmv2-pd-sane.tmp
	@echo "$(P4_PREFIX)" >> .bmv2-pd-sane.tmp
	@echo "$(P4_OPTIONS)" >> .bmv2-pd-sane.tmp
	@if test -f .bmv2-pd-sane; then :; else \
		touch .bmv2-pd-sane;\
	fi
	@if diff .bmv2-pd-sane .bmv2-pd-sane.tmp >/dev/null; then :; else \
		echo "p4c-bm env change"; \
		$(MAKE) clean; \
	fi
	@mv .bmv2-pd-sane.tmp .bmv2-pd-sane

.PHONY : pd_files-sanitize

pd_files.ts : $(P4_PATH) $(template_files) $(template_plugin_files) | pd_files-sanitize
	@rm -f pd_files.tmp
	@touch pd_files.tmp
	$(top_srcdir)/p4c_bm/__main__.py --pd $(builddir)/p4_pd/ --p4-prefix $(P4_PREFIX) $(P4_OPTIONS) $(P4_PATH)
	@mv -f pd_files.tmp $@
$(pd_files) $(plugin_files) $(pd_p4_IDL) $(pd_p4_src) : pd_files.ts
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
	$(THRIFT) -o $(builddir)/pd_thrift_gen/ -I $(top_srcdir)/pdfixed/thrift/ --gen cpp -r $(pd_p4_IDL)
	$(THRIFT) -o $(builddir)/pd_thrift_gen/ -I $(top_srcdir)/pdfixed/thrift/ --gen py -r $(pd_p4_IDL)
	mv -f pd_thrift_gen/gen-cpp/$(P4_PREFIX).h pd_thrift_gen/gen-cpp/p4_prefix.h
	sed --in-place 's/include "$(P4_PREFIX).h"/include "p4_prefix.h"/' pd_thrift_gen/gen-cpp/$(P4_PREFIX).cpp
	python $(srcdir)/split_pd_thrift.py pd_thrift_gen/gen-cpp/$(P4_PREFIX).cpp pd_thrift_gen/gen-cpp/ 3
	@mv -f pd_thrift_files.tmp $@
$(pd_thrift_files): pd_thrift_files.ts
## Recover from the removal of $@
	if test -f $@; then :; else \
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
$(pd_files) \
$(pd_thrift_files) \
$(thrift_py_lzma)

nobase_pkginclude_HEADERS = \
$(pd_headers) \
$(plugin_headers) \
p4_pd/thrift-src/pd_rpc_server.h

lib_LTLIBRARIES = libpd.la libpdthrift.la

libpd_la_SOURCES = \
$(pd_files)

libpdthrift_la_SOURCES = \
$(pd_thrift_files) \
p4_pd/thrift-src/pd_rpc_server.cpp

AM_CPPFLAGS = -I$(top_srcdir)/pdfixed/
AM_CPPFLAGS += -I$(top_srcdir)/pdfixed/src/
AM_CPPFLAGS += -I$(builddir)/pd_thrift_gen/gen-cpp/
AM_CPPFLAGS += -I$(builddir)/p4_pd/
AM_CPPFLAGS += -I$(top_builddir)/pdfixed/bmv2_thrift_gen/gen-cpp/

# Openflow plugin
if COND_PLUGIN_OPENFLOW
template_plugin_files += \
$(top_srcdir)/p4c_bm/plugin/of/src/pd_wrappers.c    \
$(top_srcdir)/p4c_bm/plugin/of/src/ofpat_groups.c   \
$(top_srcdir)/p4c_bm/plugin/of/src/ofpat_state.c    \
$(top_srcdir)/p4c_bm/plugin/of/src/ofpat_pipeline.c \
$(top_srcdir)/p4c_bm/plugin/of/inc/pd_wrappers.h    \
$(top_srcdir)/p4c_bm/plugin/of/inc/ofpat_groups.h   \
$(top_srcdir)/p4c_bm/plugin/of/src/ofpat_state.h    \
$(top_srcdir)/p4c_bm/plugin/of/inc/ofpat_pipeline.h \
$(top_srcdir)/p4c_bm/plugin/of/inc/openflow.h

of_sources = \
p4_pd/plugin/of/src/pd_wrappers.c    \
p4_pd/plugin/of/src/ofpat_groups.c   \
p4_pd/plugin/of/src/ofpat_state.c    \
p4_pd/plugin/of/src/ofpat_pipeline.c

of_includes = \
p4_pd/plugin/of/inc/pd_wrappers.h    \
p4_pd/plugin/of/inc/ofpat_groups.h   \
p4_pd/plugin/of/src/ofpat_state.h    \
p4_pd/plugin/of/inc/ofpat_pipeline.h \
p4_pd/plugin/of/inc/openflow.h

plugin_files += $(of_sources) $(of_includes)
plugin_headers += $(of_includes)

lib_LTLIBRARIES += libof.la

libof_la_SOURCES = $(of_sources) $(of_includes)

# Flags for including from p4ofagent/indigo
AM_CPPFLAGS += -D_BMV2_
AM_CPPFLAGS += -I $(builddir)/../../p4ofagent
AM_CPPFLAGS += -I $(builddir)/../../p4ofagent/inc
AM_CPPFLAGS += -I $(builddir)/../../p4ofagent/submodules/indigo/modules/indigo/module/inc
AM_CPPFLAGS += -I $(builddir)/../../p4ofagent/submodules/indigo/submodules/loxigen-artifacts/loci/inc
AM_CPPFLAGS += -I $(builddir)/../../p4ofagent/submodules/indigo/submodules/infra/modules/AIM/module/inc
AM_CPPFLAGS += -O0 -g
endif

CLEANFILES = $(BUILT_SOURCES) \
pd_files.ts pd_thrift_files.ts \
.bmv2-pd-sane
