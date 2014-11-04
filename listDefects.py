#!/usr/bin/python

import logging

from suds.client import *
from suds.wsse import *
from datetime import timedelta
from optparse import OptionParser

##########
# Basic operational SUDs stuff
##########
class Services :
	def __init__(self) :
		self.host = "http://127.0.0.1"
		self.port = "8080"
	
	def setHost(self, in_host) :
		self.host = in_host

	def getHost(self) :
		return self.host

	def setPort(self, in_port) :
		self.port = in_port
	
	def getPort(self) :
		return self.port

	def getURL(self, in_url) :
		return self.host + ":" + self.port + "/ws/v4/" + in_url + "?wsdl"

	def setServicesSecurity(self, client, in_user, in_pass) :
		security = Security()
		token = UsernameToken(in_user, in_pass)
		security.tokens.append(token)
		client.set_options(wsse=security)
		
##########
# Configuration Service (WebServices)
##########
class ConfigurationService(Services) :
	def __init__(self, in_host, in_port) :
		print "Starting ConfigurationService\n"
		self.setHost(in_host)
		self.setPort(in_port)
		self.client = Client(self.getURL("configurationservice"))
	
	def setSecurity(self, in_user, in_pass) :
		self.setServicesSecurity(self.client, in_user, in_pass)

	def create(self, in_obj) :
		return self.client.factory.create(in_obj)

	def getSnapshotsForStream(self, stream_name) :
		sido = self.client.factory.create("streamIdDataObj")
		sido.name = stream_name
		snapshots = self.client.service.getSnapshotsForStream(sido)
		return snapshots

	def getSnapshotInformation(self, snapshots) :
		snapshot_info = self.client.service.getSnapshotInformation(snapshots)
		return snapshot_info

	def getComponent(self, component_name) :
		# create a component identifier
		ciddo = self.client.factory.create("componentIdDataObj")
		ciddo.name = component_name
		return self.client.service.getComponent(ciddo)

	def doNotify(self, subscribers) :
		subject = "Notification of Receipt of Defects"
		message  = "<p>Your junk is broken</p><p>It is still broken</p>"
		message += "<a href=\"http://www.wunderground.com\">Wunderground</a>"
		self.client.service.notify(subscribers, subject, message)

##########
# Defect Service (WebServices)
##########
class DefectService(Services) :
	def __init__(self, in_host, in_port) :
		print "Starting DefectService\n"
		self.setHost(in_host)
		self.setPort(in_port)
		self.client = Client(self.getURL("defectservice"))
	
	def setSecurity(self, in_user, in_pass) :
		self.setServicesSecurity(self.client, in_user, in_pass)

	def create(self, in_obj) :
		return self.client.factory.create(in_obj)

	# This method obtains CIDs that exist in a single snapshot only
	def getSnapshotCIDs(self, stream_name, in_snapshotobj) :
		# Create a stream identifier
		sido = self.client.factory.create("streamIdDataObj")
		sido.name = stream_name

		# create the filter to specify a single snapshot only
		filterSpec = self.client.factory.create("mergedDefectFilterSpecDataObj")
		ssfsdo = self.client.factory.create("streamSnapshotFilterSpecDataObj")
		ssfsdo.snapshotIdIncludeList.append(in_snapshotobj)
		ssfsdo.streamId = sido
		filterSpec.streamSnapshotFilterSpecIncludeList.append(ssfsdo)

		# make the WebServices call to get the information
		return self.client.service.getCIDsForStreams(sido, filterSpec)

	def getMergedDefectsForStreams(self, stream_name, cids) :
		# create a stream identifier
		sido = self.client.factory.create("streamIdDataObj")
		sido.name = stream_name

		# create a filter to access the data we need for each of the CIDs
		filterSpec = self.client.factory.create("mergedDefectFilterSpecDataObj")
		filterSpec.cidList = cids

		# create a page specification object
		pageSpec = self.client.factory.create("pageSpecDataObj")
		pageSpec.pageSize = 2500
		pageSpec.sortAscending = True
		pageSpec.startIndex = 0

		# gather the information from all of the CIDs in our list
		return_cids = self.client.service.getMergedDefectsForStreams(sido, filterSpec, pageSpec)
		return return_cids

##########
# Main Entry Point
##########
def main() :
	# Configuration Information
	target_stream = options.stream
	port = options.port
	hostname = options.hostname

	username = options.username
	password = options.password

	# Begin by getting the configuration service to access the snapshot IDs
	# that have been placed in the stream of interest.
	cs = ConfigurationService("http://" + hostname, port)
	cs.setSecurity(username, password)
	ssfs = cs.getSnapshotsForStream(target_stream)

	# if we do not have any snapshots, simply return with a -1
	if len(ssfs) < 1 :
		return -1

	# Gather all CIDs relevant to this snapshot ID.  We begin by opening a
	# DefectService client.
	last_snapshot = ssfs[len(ssfs) - 1]
	ds = DefectService("http://" + hostname, port)
	ds.setSecurity(username, password)
	cids = ds.getSnapshotCIDs(target_stream, last_snapshot)

	# get the information for the CIDs.  We will review it to be sure that all
	# of the defects that are moved to our output list were found in the latest
	# snapshot only.
	unfiltered_cid_list = ds.getMergedDefectsForStreams(target_stream, cids)

	# review the list and only select ones whose "firstDetectedSnapshotId"
	# matches the last snapshot in this stream
	filtered_cid_list = [ ]
	for cid in unfiltered_cid_list.mergedDefects :
		if cid.firstDetectedSnapshotId == last_snapshot.id :
			filtered_cid_list.append(cid)
	
	# for each defect in the filtered list, 
        #      first print the content of the defect obj
	#      then print its attributes:
	#             CID#,
	#             Checker that caught the defect,
	#             Fully qualified filename where the defect is located
	for cid in filtered_cid_list :
		print cid
		print cid.cid, cid.checkerName, cid.filePathname, "\n"

	# for cid in filtered_cid_list :

	# we are done!
	print "Task Complete.\n"

##########
# Should be at bottom of "Main Entry Point".  Points the script back up into
# the appropriate entry function
##########
parser = OptionParser()
parser.add_option("-c", "--host", dest="hostname", 
                  help="Set hostname or IP address of CIM",
				  default="127.0.0.1")
parser.add_option("-p", "--port", dest="port",
				  help="Set port number to use",
				  default="8080")
parser.add_option("-u", "--user", dest="username",
				  help="Set username to perform query",
				  default="")
parser.add_option("-a", "--password", dest="password",
				  help="Set password token for the username specified",
				  default="")
parser.add_option("-s", "--stream", dest="stream",
				  help="Set target stream for access",
				  default="")
(options, args) = parser.parse_args()
if __name__ == "__main__" :
	main()
