#!/usr/bin/python
import CIM
#from csv2dictOfList import getCsvMap 
from CIM import csvfile
from getallproj import getCIMMappings
#get project/stream map from csv file
import csv
newMappings=list()
with open(csvfile) as f:
	f_csv = csv.reader(f)
	for row in f_csv:
		newMappings.append(row)

#get existing CIM mappings
CIMMappings=getCIMMappings()


for i in newMappings:
	print i
exit(0)


#projectMap=getCsvMap(csvfile)
#for project, stream in projectMap.items():
#	print project, '=>', projectMap[project]
#exit(0)

#get project list
projectsList = CIM.ConfServiceClient.service.getProjects()
for aproject in projectsList:
	print aproject.id.name

#create a project
projectSpec = CIM.ConfServiceClient.factory.create("projectSpecDataObj")
projectSpec.description = "Testing web services";
projectSpec.name = "Test00";
CIM.ConfServiceClient.service.createProject(projectSpec)
print "\n-----------------List of Projects:"


