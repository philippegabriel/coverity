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
csv:=$(call config,'csvfile')
params:=--host $(host) --port $(port) --user $(user) --password $(pass) --csvfile $(csv)
getallproj:
	python getallproj.py $(params)
createproj:
	python createproject.py $(params)
getcompmaps:
	python getComponentMaps.py  $(params)




