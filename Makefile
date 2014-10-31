#philippeg oct2014
#
#various utilities to administer the Coverity CIM, through the SOAP apis
#See: cov_platform_web_service_api_ref.html
#
.PHONY: getallproj createproj getcompmaps
SELF_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
configFile:=$(SELF_DIR)/.config
# Read config params from .config file
config=$(lastword $(shell grep $(1) $(configFile)))
host:=$(call config,'host')
port:=$(call config,'port')
user:=$(call config,'username')
pass:=$(call config,'password')
projcsv:=testProjectAndStreams.csv
cmcsv:=testComponentMap.csv
getprojects:
	python getProjects.py --host $(host) --port $(port) --user $(user) --password $(pass)
createproj:
	python createproject.py --host $(host) --port $(port) --user $(user) --password $(pass) < $(projcsv) 
getcompmaps:
	python getComponentMaps.py  --host $(host) --port $(port) --user $(user) --password $(pass)
createcompmap:
	python createComponentMap.py --host $(host) --port $(port) --user $(user) --password $(pass) < $(cmcsv)
query:
	python query.py --host $(host) --port $(port) --user $(user) --password $(pass)
testing: 
	make clean 
	@echo '=================================[Testing Create Project & Streams...]=================='
	make createproj 
	make getprojects | grep '000' | sort > /tmp/out.csv
	grep -v '#' $(projcsv)  | sort > /tmp/in.csv
	diff -B /tmp/in.csv /tmp/out.csv
	@echo '=========================================[Test PASS]========================================='
	@echo '=================================[Testing Create Component maps...]======================'
	make createcompmap
	make getcompmaps | grep '000' | sort > /tmp/out.csv
	grep -v '#' $(cmcsv)  | sort > /tmp/in.csv
	diff -B /tmp/in.csv /tmp/out.csv
	@echo '=========================================[Test PASS]========================================='
clean:
	rm -f *.pyc
	python rmproject.py --host $(host) --port $(port) --user $(user) --password $(pass) < $(projcsv)
	python rmComponentsMaps.py --host $(host) --port $(port) --user $(user) --password $(pass) < $(cmcsv)
test:
	python test.py < $(projcsv)





