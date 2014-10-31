#!/usr/bin/python
#use Coverity SOAP method to create a component map
#see: cov_platform_web_service_api_ref.html, 
#methods createComponentMap & getComponentMaps & updateComponentMap
#
#input is a dsl on stdin
#dsl definition:
#map,<map id>,<description>
#bind,<map id>,<component id>,regexp

import sys,csv,suds,CIM
#skip blank lines
input = filter(lambda x: x, csv.reader(sys.stdin))
#Extract map, bindings
maps=filter(lambda x: x[0] == 'map', input)
binds =filter(lambda x: x[0] == 'bind', input)

for i in maps:
	mapspec = CIM.ConfServiceClient.factory.create('componentMapSpecDataObj')
	mapspec.componentMapName=i[1]
	mapspec.description=i[2]
	try:
		CIM.ConfServiceClient.service.createComponentMap(mapspec)
	except suds.WebFault as f:
#See, cov_platform_web_service_api_ref.html#TP-Error_Codes-Error_Codes "1610 Component map exists already"
		if f.fault.detail.CoverityFault.errorCode in ['1610']:
			print 'Warning: %s %s' % (f.fault.detail.CoverityFault.errorCode,f.fault.faultstring)
			continue
		else:
			sys.exit(f.fault) 
		
#Create the componentMapSpec object
for i in binds:
#create the dependent objects
		mapId = CIM.ConfServiceClient.factory.create('componentMapIdDataObj')
		mapId.name=i[1]
		compid = CIM.ConfServiceClient.factory.create('componentIdDataObj')
		compid.name = i[1]+'.'+i[2]
		pathRules = CIM.ConfServiceClient.factory.create('componentPathRuleDataObj')
		pathRules.pathPattern = i[3]
		pathRules.componentId=compid
		component = CIM.ConfServiceClient.factory.create('componentDataObj')
		component.componentId=compid
#Retrieve the existing component map
		filter = CIM.ConfServiceClient.factory.create("componentMapFilterSpecDataObj")
		filter.namePattern=i[1]
		currentmapspecList = CIM.ConfServiceClient.service.getComponentMaps(filter)
#assert list is singleton
		assert(len(currentmapspecList) == 1)
		currentmapspec=list.pop(currentmapspecList)
		try:
			x=len(currentmapspec.componentPathRules)
		except:
			x=0
			pass
		print '####%s,%s,%d'%(currentmapspec.componentMapId.name,currentmapspec.description,x)
#Create new component
		mapspec = CIM.ConfServiceClient.factory.create('componentMapSpecDataObj')
		mapspec.componentMapName=i[1]
#add existing spec
		try:
			mapspec.componentPathRules.append(currentmapspec.componentPathRules)
		except:
			pass
		try:
			mapspec.components.append(currentmapspec.component)
		except:
			pass
		try:
			mapspec.description=currentmapspec.description
		except:
			pass
#Add new component and path
		mapspec.components.append(component)
		mapspec.componentPathRules.append(pathRules)
#All newly created map, must have an 'Other' component. See Error 1604
		compOtherid = CIM.ConfServiceClient.factory.create('componentIdDataObj')
		compOtherid.name = i[1]+'.Other'
		componentOther = CIM.ConfServiceClient.factory.create('componentDataObj')
		componentOther.componentId=compOtherid
		mapspec.components.append(componentOther)

		#Send the SOAP request
		try:
			CIM.ConfServiceClient.service.updateComponentMap(mapId,mapspec)
		except suds.WebFault as f:
			sys.exit(str(f.fault))
		except Exception, e: 
			sys.exit(str(e))
exit(0)

	

