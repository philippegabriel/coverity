#!/usr/bin/python
#Dump component maps from a Coverity CIM, using the SOAP apis
#see: cov_platform_web_service_api_ref.html
import CIM
def getComponentMaps():
	mappings=list()
	filter = CIM.ConfServiceClient.factory.create("componentMapFilterSpecDataObj")
	filter.namePattern='*'
	cmList = CIM.ConfServiceClient.service.getComponentMaps(filter)
	for i in cmList:
		mapName=i.componentMapId.name
#emit component Maps definitions
		mappings.append(['map,'+mapName+','+(i.description if i.description else '')])
		try:
			rules=i.componentPathRules
			for j in rules:
#				remove the '.' + mapname that Coverity adds to the component name
				componentName=j.componentId.name.replace(mapName+'.', '') 
#emit component names and paths (as regexp)
				mappings.append(['bind,'+mapName+','+componentName+','+(j.pathPattern if j.pathPattern else '')])
		except:
			pass
	return mappings
#main
myMappings=getComponentMaps()
for i in myMappings:
	print ','.join(map(str,i))
exit(0)


