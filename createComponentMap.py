#!/usr/bin/python
#use Coverity SOAP method to create a component map
#Relevant bit of SOAP:
#
#<componentMapSpec>
#   <componentMapName>test00</componentMapName>
#   <componentPathRules>
#      <componentId>
#         <name>test00.c00</name>
#      </componentId>
#      <pathPattern>/test/</pathPattern>
#   </componentPathRules>
#   <components>
#      <componentId>
#         <name>test00.c00</name>
#      </componentId>
#   </components>
#   <defectRules>
#      <componentId>
#         <name>test00.c00</name>
#      </componentId>
#   </defectRules>
#   <description>test00</description>
#</componentMapSpec>

import sys
import CIM
from CIM import csvfile
#get component map from csv file
import csv
newMap=list()
try:
	f=open(csvfile)
except:
	sys.exit('Cannot find '+csvfile)
#Create the componentMapSpec object
mapspec = CIM.ConfServiceClient.factory.create("componentMapSpec")
f_csv = csv.reader(f)
for row in f_csv:
	if row==[]:
		continue
	if row[0] == 'map':
		mapspec.componentMapName=row[1]
		mapspec.description=row[2]
	elif row[0] == 'bind':
#skip row[1] assumed to be map name
		pathrules = CIM.ConfServiceClient.factory.create("componentPathRuleDataObj")
		component = CIM.ConfServiceClient.factory.create("componentDataObj")
		defectrules = CIM.ConfServiceClient.factory.create("componentDefectRuleDataObj")
		compid = CIM.ConfServiceClient.factory.create("componentIdDataObj")
		compid.name = mapspec.componentMapName+'.'+row[2]
		pathrules.pathPattern = row[3]
		pathrules.componentId=compid
		mapspec.componentPathRules.append(pathrules)
		component.componentId=compid
		mapspec.components.append(component)
		defectrules.componentId=compid
		mapspec.defectRules.append(defectrules)
#Send the SOAP request
try:
	CIM.ConfServiceClient.service.createComponentMap(mapspec)
except:
	sys.exit('createComponentMap request failed')
exit(0)

	

