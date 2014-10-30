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

#
#Bind streams
#
for bind in binds:
	try:
#Prior to bind streams to project, retrieve the existing bindings
		filter = CIM.ConfServiceClient.factory.create("projectFilterSpecDataObj")
		filter.namePattern=bind[1]
		filter.includeStreams=1
		projectList = CIM.ConfServiceClient.service.getProjects(filter)
#assert list is singleton
		assert(len(projectList) == 1)
		project=list.pop(projectList)
		projectId = project.id
		try:
			streams = map(lambda x: x.id , project.streams)
		except AttributeError:
			streams = list()
		try:
			streamLinks = map(lambda x: x.id , project.streamLinks)
		except AttributeError:
			streamLinks = list()
		print bind,streams
		projectSpec = CIM.ConfServiceClient.factory.create("projectSpecDataObj")
		stream = CIM.ConfServiceClient.factory.create("streamIdDataObj")
		stream.name = bind[2]
		streams.append(stream)
		projectSpec.streams=streams
		projectSpec.streamLinks=streamLinks
		CIM.ConfServiceClient.service.updateProject(projectId,projectSpec)
	except suds.WebFault as f:
		sys.exit(f.fault) 
#
#Link streams
# same as Bind, except for s/project.streams/project.streamLinks /
#
for link in links:
	try:
#Prior to bind streams to project, retrieve the existing bindings
		filter = CIM.ConfServiceClient.factory.create("projectFilterSpecDataObj")
		filter.namePattern=link[1]
		filter.includeStreams=1
		projectList = CIM.ConfServiceClient.service.getProjects(filter)
#assert list is singleton
		assert(len(projectList) == 1)
		project=list.pop(projectList)
		projectId = project.id
		try:
			streams = map(lambda x: x.id , project.streams)
		except AttributeError:
			streams = list()
		try:
			streamLinks = map(lambda x: x.id , project.streamLinks)
		except AttributeError:
			streamLinks = list()
		print link,streams
		projectSpec = CIM.ConfServiceClient.factory.create("projectSpecDataObj")
		stream = CIM.ConfServiceClient.factory.create("streamIdDataObj")
		stream.name = link[2]
		streamLinks.append(stream)
		projectSpec.streams=streams
		projectSpec.streamLinks=streamLinks
		CIM.ConfServiceClient.service.updateProject(projectId,projectSpec)
	except suds.WebFault as f:
		sys.exit(f.fault) 
exit(0)

