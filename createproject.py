#!/usr/bin/python
import sys,csv,suds
import CIM
#from csv2dictOfList import getCsvMap 
from CIM import csvfile
newMappings=list()
try:
	f=open(csvfile)
except:
	sys.exit('Cannot find '+csvfile)
#skip blank lines
newMappings = filter(lambda x: x, csv.reader(f))
#Extract projects, streams, bind, links
projects=filter(lambda x: x[0] == 'project', newMappings)
streams =filter(lambda x: x[0] == 'stream', newMappings)
links   =filter(lambda x: x[0] == 'link', newMappings)
binds   =filter(lambda x: x[0] == 'bind', newMappings)

#
#Create projects
#
for project in projects:
	projectSpec = CIM.ConfServiceClient.factory.create("projectSpecDataObj")
	projectSpec.name = project[1]
	projectSpec.description = project[2]
	try:
		CIM.ConfServiceClient.service.createProject(projectSpec)
	except suds.WebFault as f:
		if f.fault.detail.CoverityFault.errorCode in ['1303']:
#printout the error 
			print 'Warning: %s %s' % (f.fault.detail.CoverityFault.errorCode,f.fault.faultstring)
			continue
		else:
			sys.exit(f.fault) 
#
#Create streams
#
for stream in streams:
	streamSpec = CIM.ConfServiceClient.factory.create("streamSpecDataObj")
	streamSpec.name = stream[1]
	streamSpec.description = stream[2]
	streamSpec.componentMapId=CIM.ConfServiceClient.factory.create("componentMapIdDataObj")
	streamSpec.componentMapId.name='xenserver'
	streamSpec.triageStoreId=CIM.ConfServiceClient.factory.create("triageStoreIdDataObj")
	streamSpec.triageStoreId.name='Default Triage Store'
	try:
		CIM.ConfServiceClient.service.createStream(streamSpec)
	except suds.WebFault as f:
		if f.fault.detail.CoverityFault.errorCode in ['1301']:
#printout the error 
			print 'Warning: %s %s' % (f.fault.detail.CoverityFault.errorCode,f.fault.faultstring)
			continue
		else:
			sys.exit(f.fault) 
exit(0)


