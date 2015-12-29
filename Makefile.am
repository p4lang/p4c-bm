ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS} -I m4
PDFIXED_LIBS := libpdfixed.la libpdfixedthrift.la

all-local: $(PDFIXED_LIBS)

$(PDFIXED_LIBS) :
	@make -C pd_mk libpdfixed.la
	@make -C pd_mk libpdfixedthrift.la

# Ideally, Makefile inside pd_mk should be used.. but it is mixed up with other targets that
# cannot be built at this time
install-exec-local:
	$(PYTHON) $(srcdir)/setup.py install --prefix $(DESTDIR)$(prefix)
	@mkdir -p /usr/local/include/p4c_bm/pd
	@cp pdfixed/pd/*.h /usr/local/include/p4c_bm/pd
	@cp pdfixed/src/*.h /usr/local/include/p4c_bm/pd
	@mkdir -p /usr/local/lib/p4c_bm/pd
	@cp pd_mk/.libs/libpdfixed.a pd_mk/.libs/libpdfixedthrift.a /usr/local/lib/p4c_bm/pd
