#!/usr/bin/python
#See: https://communities.coverity.com/message/2836#2836

#================================Get CLI params======================================
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-c", "--host", dest="host", help="Set hostname or IP address of CIM",  default="")
parser.add_option("-p", "--port", dest="port",	   help="Set port number to use",			  default="")
parser.add_option("-u", "--user", dest="username", help="Set username to perform query",      default="admin")
parser.add_option("-a", "--password", dest="password",  help="Set password token for the username specified",  default="")
parser.add_option("-s", "--stream", dest="stream", 	  help="Set target stream for access",	  default="")
parser.add_option("-f", "--csvfile", dest="csv", 	  help="csv file: project/stream map",	  default="")
(options, args) = parser.parse_args()
target_stream = options.stream

#=================================housekeeping=====================================
import socket
socket.setdefaulttimeout(None)
import suds,logging
logging.basicConfig(level=logging.CRITICAL)
logging.getLogger("suds.client").setLevel(logging.CRITICAL)
CURSOR=None
csvfile=options.csv
#=================================setup services===================================
MyUrl="http://"+options.host+":"+options.port
#Seems deprecated in v8
#MyAdmSrv=MyUrl+	"/ws/v8/administrationservice?wsdl"
#http://dagu-4.uk.xensource.com:8080/ws/v8/configurationservice?wsdl
MyConfSrv=MyUrl+"/ws/v8/configurationservice?wsdl"
#http://dagu-4.uk.xensource.com:8080/ws/v8/defectservice?wsdl
MyDefSrv=MyUrl+"/ws/v8/defectservice?wsdl"
#Setup authorization
Security = suds.wsse.Security()
Security.tokens.append(suds.wsse.UsernameToken(options.username,options.password))
#Administration Service Client - Users, Groups, Roles
#AdminServiceClient = suds.client.Client(MyAdmSrv, timeout=3600)
#AdminServiceClient.set_options(wsse=Security)
#Configuration Service Client - Projects, Streams, Component Maps, Snapshots and Defect Attributes
ConfServiceClient = suds.client.Client(MyConfSrv, timeout=3600)
ConfServiceClient.set_options(wsse=Security)
#Defect Service Client - Defects and Defect Instances
DefServiceClient = suds.client.Client(MyDefSrv, timeout=3600)
DefServiceClient.set_options(wsse=Security)
#=================================end setup services===================================
