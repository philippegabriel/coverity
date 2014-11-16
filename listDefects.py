#!/usr/bin/python

from suds.client import *
from suds.wsse import *

from CIM import *

##########
# Configuration Service (WebServices)
##########
class ConfigurationService() :
	def __init__(self, ConfServiceClient) :
		print "Starting ConfigurationService\n"
                self.client = ConfServiceClient

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
class DefectService() :
	def __init__(self) :
		print "Starting DefectService\n"
                # FIXME: looks like coverity different ws versions not compatible
                MyDefSrvUrl=MyUrl+"/ws/v4/defectservice?wsdl"
		self.client = suds.client.Client(MyDefSrvUrl, timeout=3600)
                self.client.set_options(wsse=Security)

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

	# Begin by getting the configuration service to access the snapshot IDs
	# that have been placed in the stream of interest.
	cs = ConfigurationService(ConfServiceClient)
	ssfs = cs.getSnapshotsForStream(target_stream)

	# if we do not have any snapshots, simply return with a -1
	if len(ssfs) < 1 :
		return -1

	# Gather all CIDs relevant to this snapshot ID.  We begin by opening a
	# DefectService client.
	last_snapshot = ssfs[len(ssfs) - 1]
	ds = DefectService()
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

if __name__ == "__main__" :
	main()
