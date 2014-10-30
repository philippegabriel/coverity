#!/usr/bin/python
#Common definition for Coverity CIM SOAP methods
#see: cov_platform_web_service_api_ref.html
#See: https://communities.coverity.com/message/2836#2836

#================================Get CLI params======================================
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-c", "--host", dest="host", help="Set hostname or IP address of CIM",  default="")
parser.add_option("-p", "--port", dest="port",	   help="Set port number to use",			  default="")
parser.add_option("-u", "--user", dest="username", help="Set username to perform query",      default="admin")
parser.add_option("-a", "--password", dest="password",  help="Set password token for the username specified",  default="")
(options, args) = parser.parse_args()

#=================================housekeeping=====================================
import suds,logging
logging.basicConfig(level=logging.CRITICAL)
logging.getLogger("suds.client").setLevel(logging.CRITICAL)
CURSOR=None
#=================================setup services===================================
MyUrl="http://"+options.host+":"+options.port
MyConfSrv=MyUrl+"/ws/v8/configurationservice?wsdl"
MyDefSrv=MyUrl+"/ws/v8/defectservice?wsdl"
#Setup authorization
Security = suds.wsse.Security()
Security.tokens.append(suds.wsse.UsernameToken(options.username,options.password))
#Configuration Service Client - Projects, Streams, Component Maps, Snapshots and Defect Attributes
ConfServiceClient = suds.client.Client(MyConfSrv, timeout=3600)
ConfServiceClient.set_options(wsse=Security)
#Defect Service Client - Defects and Defect Instances
DefServiceClient = suds.client.Client(MyDefSrv, timeout=3600)
DefServiceClient.set_options(wsse=Security)
#=================================end setup services===================================
