#!/usr/bin/python
#use Coverity SOAP method to create a component map
#see: cov_platform_web_service_api_ref.html, 
#methods deleteComponentMap
#
#input is a dsl on stdin
#dsl definition:
#map,<map id>,<description>
#bind,<map id>,<component id>,regexp

import sys,csv,suds,CIM
#skip blank lines
input = filter(lambda x: x, csv.reader(sys.stdin))
#Extract map, bindings
maps = filter(lambda x: x[0] == 'map', input)

for i in maps:
#Retrieve the existing component map
	componentMapId = CIM.ConfServiceClient.factory.create("componentMapIdDataObj")
	componentMapId.name=i[1]
	try:
		CIM.ConfServiceClient.service.deleteComponentMap(componentMapId)
	except suds.WebFault as f:
#See, cov_platform_web_service_api_ref.html#TP-Error_Codes-Error_Codes "1600 No valid component map found"
		if f.fault.detail.CoverityFault.errorCode in ['1600']:
			print 'Warning: %s %s' % (f.fault.detail.CoverityFault.errorCode,f.fault.faultstring)
			continue
		else:
			sys.exit(f.fault) 
exit(0)

	

