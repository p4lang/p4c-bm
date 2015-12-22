install:
	@python setup.py install
	@mkdir -p /usr/local/include/p4c_bm/pd
	@cp pdfixed/pd/*.h /usr/local/include/p4c_bm/pd
	@cp pdfixed/src/*.h /usr/local/include/p4c_bm/pd
