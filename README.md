## Description

Utilities to interact with the Coverity CIM via the SOAP api. See: http://www.coverity.com

Coverity documents a SOAP api, to interact with the Coverity "Connect" server.
See: `/docs/en/api/cov_platform_web_service_api_ref.html`

This repo contains a set of python scripts, to:
* Get all **project** and associated **streams** from the server
* Create **project** and **streams** and bind them
* Get the **ComponentMaps** and associated **components** and **path rules** from the server
* Create **ComponentMaps**, **components** and **path rules** and bind them

The input for the create script is a csv file, which defines a trivial dsl, defined as:
```
#project and stream commands
project,<project id>,<description>
stream,<stream id>,<description>
bind,<project id>,<stream id>
link,<project id>,<stream id>
#Component map commands
map,<map id>,<description>
bind,<map id>,<component id>,regexp
```
See: `testComponentMap.csv` & `testProjectAndStreams.csv` and the **testing** target in the `Makefile`

## Prequisites
* Python (tested with 2.7.6) running on Ubuntu 14.04
* Python suds module (tested with 0.4)

## installation
1. Clone this repo
2. Create a `.config` file, that contains the address of the Coverity server and the credentials for a user allowed to create project, streams and ComponentMaps

The `.config` file has the following syntax:
```
host		<Coverity server dns name>
port		<Coverity server port number, usually 8080>
username	<username>
password	<pass>
```
Test the setup with ```make testing```

## troubleshooting
Refer to Coverity documentation `docs/en/api/cov_platform_web_service_api_ref.html#TP-Error_Codes-Error_Codes`

