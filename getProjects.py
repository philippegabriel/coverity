#!/usr/bin/python
#
#Dump projects and streams from a Coverity CIM on stdout using the SOAP apis
#see: cov_platform_web_service_api_ref.html, methods getProjects & getStreams
#
import sys, CIM
#emit project definitions
def getCIMMappings():
	mappings=list()
	projectsList = CIM.ConfServiceClient.service.getProjects()
	for i in projectsList:
		item=['project',i.id.name]
		try:
			item.append(i.description)
		except AttributeError:
			item.append('')
		mappings.append(item)
#emit stream definitions
	streamsList = CIM.ConfServiceClient.service.getStreams()
	for i in streamsList:
		item=['stream',i.id.name]
		try:
			item.append(i.description)
		except AttributeError:
			item.append('')
		mappings.append(item)
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


