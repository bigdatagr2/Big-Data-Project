#!/bin/bash
#cd /media/FREEBOX/GITHUB
y=0
for x in /media/FREEBOX/GITHUB/*.gz ;
do
	if [ $y -lt -1 ]
	then	
		break
	else
		echo -e $x"\n";
		rm ./x*
		zcat $x | split -l 10000 ;
		for xsplit in ./x*;
		do
			printf "%s\n" "split is :$xsplit" ; echo -e "\n"
			#cat $xsplit | jq -c '. | {"index": {"_index": "github", "_type":"data", "_id": .id }}, .'
			printf "%0.s-" {1..60}; echo -e "\n"
			cat $xsplit | jq -c '. | {"index": {"_index": "github", "_type":"data", "_id": .id }}, .' | curl -XPOST 192.168.39.23:9200/_bulk  -# -H 'Content-Type: application/json' --data-binary @-
#			zcat $xsplit | while read line;
#			do
#				
#				#echo $line | jq -c '. | {"index": {"_index": "github", "_type":"data", "_id": .id }}, .'
#				printf "%0.s-" {1..60} + "\n"
#				#echo $line | jq -c '. | {"index": {"_index": "github", "_type":"data", "_id": .id }}, .' | curl -XPOST 192.168.39.23:9200/_bulk -H 'Content-Type: application/json' --data-binary @-
#				echo $line | curl -XPOST 192.168.39.23:9200/github/data -H 'Content-Type: application/json' --data-binary @-
#			done
			
		done
		
		((++y))	
	fi
	echo -e "Fichier à enlever :  $x \n"
	rm $x 
	echo -e "Fichier supprimé : $x \n"
done


