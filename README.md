## Description

Utilities to interact with the Coverity CIM via the SOAP api. See: http://www.coverity.com

Coverity documents a SOAP api, to interact with the Coverity "Connect" server.
See: `/docs/en/api/cov_platform_web_service_api_ref.html`

This repo contains a set of python scripts, to:
* Get all **projects** and associated **streams** from the server
* Create **projects** and **streams** and bind them
* Get the **ComponentMaps** and associated **components** and **path rules** from the server
* Create **ComponentMaps**, **components** and **path rules** and bind them

Scripts input is a csv file, which defines a trivial dsl:
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

### Python Environment Setup on CentOS 6
1.  yum install zlib-devel wget gcc ncurses-devel readline-devel openssl openssl-devel bzip2-devel sqlite-devel gdbm-devel
2.  cd /usr/local
3.  wget http://www.python.org/ftp/python/2.7/Python-2.7.tgz
4.  tar xvzf Python-2.7.tgz
5.  cd Python-2.7
6.  ./configure
7.  make
8.  make install
9.  cd /usr/local/
10. wget http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg
11. sh setuptools-0.6c11-py2.7.egg
12. easy_install suds    ## Python SOAP client

## Installation
1. Clone this repo
2. Create a `.config` file, that contains the address of the Coverity server and the credentials for a user allowed to create project, streams and ComponentMaps

The `.config` file has the following syntax:
```
host		<Coverity server dns name>
port		<Coverity server port number, usually 8080>
username	<username>
password	<pass>
stream          <stream name>
```
Test the setup with ```make testing```

## Troubleshooting
Refer to Coverity documentation `docs/en/api/cov_platform_web_service_api_ref.html#TP-Error_Codes-Error_Codes`

