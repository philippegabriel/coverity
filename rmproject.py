#!/usr/bin/python
#
#Delete projects and streams from a Coverity CIM, using the SOAP apis
#see: cov_platform_web_service_api_ref.html, deleteProject & deleteStream methods
#
import sys,csv,suds,CIM
#skip blank lines
input = filter(lambda x: x, csv.reader(sys.stdin))
#Extract projects, streams, bind, links
projects=filter(lambda x: x[0] == 'project', input)
streams =filter(lambda x: x[0] == 'stream', input)

#
#Delete projects
#
for project in projects:
	projectId = CIM.ConfServiceClient.factory.create("projectIdDataObj")
	projectId.name = project[1]
	try:
		CIM.ConfServiceClient.service.deleteProject(projectId)
	except suds.WebFault as f:
		if f.fault.detail.CoverityFault.errorCode in ['1302']:
#printout the error 
			print 'Warning: %s %s' % (f.fault.detail.CoverityFault.errorCode,f.fault.faultstring)
			continue
		else:
			sys.exit(f.fault) 
#
#Delete streams
#
for stream in streams:
	streamId = CIM.ConfServiceClient.factory.create("streamIdDataObj")
	streamId.name = stream[1]
	try:
		CIM.ConfServiceClient.service.deleteStream(streamId)
	except suds.WebFault as f:
		if f.fault.detail.CoverityFault.errorCode in ['1300']:
#printout the error 
			print 'Warning: %s %s' % (f.fault.detail.CoverityFault.errorCode,f.fault.faultstring)
			continue
		else:
			sys.exit(f.fault) 
exit(0)


