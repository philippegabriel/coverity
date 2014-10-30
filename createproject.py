#!/usr/bin/python
#
#Create projects and streams in Coverity CIM
#see: cov_platform_web_service_api_ref.html, methods getProjects & getStreams
#
#input is a dsl read on stdin
#dsl definition:
#project,<project id>,<description>
#stream,<stream id>,<description>
#bind,<project id>,<stream id>
#link,<project id>,<stream id>
#
import sys,csv,suds,CIM
#skip blank lines
input = filter(lambda x: x, csv.reader(sys.stdin))
#Extract projects, streams, bind, links
projects=filter(lambda x: x[0] == 'project', input)
streams =filter(lambda x: x[0] == 'stream', input)
links   =filter(lambda x: x[0] == 'link', input)
binds   =filter(lambda x: x[0] == 'bind', input)

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
for i in binds+links:
	try:
#Prior to bind streams to project, retrieve the existing bindings
		filter = CIM.ConfServiceClient.factory.create("projectFilterSpecDataObj")
		filter.namePattern=i[1]
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
		projectSpec = CIM.ConfServiceClient.factory.create("projectSpecDataObj")
		stream = CIM.ConfServiceClient.factory.create("streamIdDataObj")
		stream.name = i[2]
		if i[0]=='bind':
			streams.append(stream)
		elif i[0]=='link':
			streamLinks.append(stream)
		else:
			assert(0)
		projectSpec.streams=streams
		projectSpec.streamLinks=streamLinks
		CIM.ConfServiceClient.service.updateProject(projectId,projectSpec)
	except suds.WebFault as f:
		sys.exit(f.fault) 
exit(0)

