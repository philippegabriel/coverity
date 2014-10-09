#!/usr/bin/python
#Dump projects and streams from a Coverity CIM, using the SOAP apis
#see: cov_platform_web_service_api_ref.html
import CIM
#emit project definitions
def getCIMMappings():
	mappings=list()
	projectsList = CIM.ConfServiceClient.service.getProjects()
	for i in projectsList:
		mappings.append(['project',i.id.name,(i.description if i.description else '')])
#emit stream definitions
	streamsList = CIM.ConfServiceClient.service.getStreams()
	for i in streamsList:
		mappings.append(['stream',i.id.name,(i.description if i.description else '')])
#emit project/stream bindings
	for i in projectsList:
		try:
			for j in i.streams:
				mappings.append(['bind',i.id.name,j.id.name])
		except:
			pass
#emit project/stream links
		try:
			for j in i.streamLinks:
				mappings.append(['link',i.id.name,j.id.name])
		except:
			pass
	return mappings
#main
myMappings=getCIMMappings()
for i in myMappings:
	print ','.join(map(str,i))
exit(0)


