#!/bin/bash
cd /media/FREEBOX/GITHUB
y=0
for x in ./*.gz ;
do
	if [ $y -lt -1 ]
	then	
		break
	else
		echo $x;
		zcat $x | while read line;
		do
			
			#echo $line | jq -c '. | {"index": {"_index": "github", "_type":"data", "_id": .id }}, .'
			printf "%0.s-" {1..60} + "\n"
			#echo $line | jq -c '. | {"index": {"_index": "github", "_type":"data", "_id": .id }}, .' | curl -XPOST 192.168.39.23:9200/_bulk -H 'Content-Type: application/json' --data-binary @-
			echo $line | curl -XPOST 192.168.39.23:9200/github/data -H 'Content-Type: application/json' --data-binary @-
		done
		((++y))	
	fi
done


