ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS} -I m4

if COND_PD_MK
    MAYBE_PD_MK = pd_mk
endif

SUBDIRS = . pdfixed $(MAYBE_PD_MK)

# Inspired by https://blog.kevin-brown.com/programming/2014/09/24/combining-autotools-and-setuptools.html

# note that 'dist' commands are not supported

# not using build, because it may conflict when someone simply runs setup.py
BUILD_SUBDIR=build_setuptools

# See http://www.gnu.org/software/autoconf/manual/autoconf-2.69/html_node/Installation-Directory-Variables.html
edit = sed \
	-e 's|@pkgdatadir[@]|$(pkgdatadir)|g'

p4c_bm/config.py: $(srcdir)/p4c_bm/config.py.in Makefile
	rm -f $@ $@.tmp
	$(edit) $< >$@.tmp
	chmod a-w $@.tmp
	mv $@.tmp $@

all-local: p4c_bm/config.py
	(cd $(srcdir); $(PYTHON) setup.py build \
		--build-base $(shell readlink -f $(builddir))/$(BUILD_SUBDIR) \
		--verbose)

# For install and clean, the build command has to be repeated, otherwise -b (or
# --build-base) will be ignored

install-exec-local:
	(cd $(srcdir); $(PYTHON) setup.py build \
		-b $(shell readlink -f $(builddir))/$(BUILD_SUBDIR) \
		install \
		--prefix $(DESTDIR)$(prefix) \
		--single-version-externally-managed \
		--record $(DESTDIR)$(pkgpythondir)/install_files.txt \
		--verbose)

uninstall-local:
	cat $(DESTDIR)$(pkgpythondir)/install_files.txt | xargs rm -rf; \
	rm -rf $(DESTDIR)$(pkgpythondir)

# ideally egg_info would be deleted by setup.py clean
clean-local:
	(cd $(srcdir); $(PYTHON) setup.py build \
		-b $(shell readlink -f $(builddir))/$(BUILD_SUBDIR) \
		clean --all \
		--verbose); \
	rm -rf $(builddir)/$(BUILD_SUBDIR)/p4c_bm.egg-info
