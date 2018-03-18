# 1. DATABASE
===================

# Data download for elasticsearch

- Using githubarchives files

choice Motivation :

* Commits
* detail of the events

- Download method:
* Script bash

wget -c http://data.githubarchive.org/{2016..2018}-{01..12}-{01..31}-{0..23}.json.gz

# Elasticsearch server configuration

- Docker
- Kibana
- dockerfile
- Server environment:

* Elasticsearch version 6.2
* Kibana
* Logstash

# Creation and indexing of the database

- github index  configuration 
- indexation script

* use of gzip + zcat
* REST api d’elasticsearch
* python script : by Post web requests
* sending slices of 10,000 lines
* automatic creation of metadata before POST

# Server calibration and mapping

- reduction number of shards
- reduction name of replicas
- remodeling of the mapping

* remove nested index with "ignore above: 250" which explodes the number of fields
* creation dynamic templates des mapping

- increase of mapping.total_fields.limit to 2000

# Server calibration and mapping (2)

- Saturation of the server:
- Mapping: limitation of the text fields, privilegier the keyword
- reindexation with alias
- mapping analysis
* by script
* On Kibana

- attempt to remove from index fields ending with * url without the index

# 2. GENERATOR OF COMMITS AND RANDOM FILES

# Test the database, query and calibrate

- Test of aggregates on terms

* Event types
* Repositories
* Users
* language ...

- removal of unassigned_shards
- change of refresh_interval to boost indexing
- Storage overflow above 80% free space (88 Gb) - goes into readonly mode, disable_allocation
- normal mode recovery - parameter: index.routing.allocation.disable_allocation ": False

# Web server creation and configuration

- subscription to a web server type EC2 amazon AWS
- SSH access with shared public key
- flask server installation with python 2.7
- port opening setting 5000 for all net 0.0.0.0, :: / 0
- installation of jupyter notebook with opening ports 9999 for all net 0.0.0.0, :: / 0
- installation of the necessary python libraries
- Using socketio to display POST data in realtime
- Sending data to MQTT

# Random generation of commits and queues

- Python script from the elasticsearch server
- launch in background process with nohup
- send in post random commits from the elasticsearch database
- reception and processing at the Flask web server
- real time display of commits by websockets (limited to 10 lines then flush)
- transmission of the content to the MQTT server with different topic according to Repository and Event Type.
- Subscription tested by MQTTFX, MQTT client linux

# MQTT server creation and configuration

- subscription to a web server type EC2 amazon AWS
- SSH access with shared public key
- docker installation mqtt eclipse mosquitto, with publish ports
- port opening parameter 1883 and 9001 for all net 0.0.0.0/::00
- attempt to use HTTPS websocket in 8000, inconclusive for HIVEMQTT web client connection test

# CONCLUSION

- Elasticsearch : [http://88.169.46.187:9200/](http://88.169.46.187:9200/)
- Ichibana: 'h tp: // 88.169.46.187: 5601 / (h tp: // 88.169.46.187: 9200 /)
- Web server: [http://34.215.22.13:5000/](http://34.215.22.13:5000/)
- MQTT server: 18.188.23.129:1883

