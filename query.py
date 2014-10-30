#!/usr/bin/python
import sys,csv,suds
import CIM
filter = CIM.ConfServiceClient.factory.create("triageStoreFilterSpecDataObj")
filter.namePattern='*'
try:
	print CIM.ConfServiceClient.service.getTriageStores(filter)
except suds.WebFault as f:
	sys.exit(f.fault) 
exit(0)


