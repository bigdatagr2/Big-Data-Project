#!/bin/bash
#cd /media/FREEBOX/GITHUB
#creates a new file descriptor 3 that redirects to 1 (STDOUT)
exec 3>&1
y=0
for x in `ls /media/FREEBOX/GITHUB/2018*.gz -v` ;
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
			echo -e "\n"; printf "%s\n" "split is :$xsplit" ; echo -e "\n"
			#cat $xsplit | jq -c '. | {"index": {"_index": "github", "_type":"data", "_id": .id }}, .'
			echo -e "\n$(date)\n"; printf "%0.s-" {1..60}; echo -e "\n"
			cat $xsplit | jq -c '. | {"index": {"_index": "github", "_type":"data", "_id": .id }}, .' |gzip -c | HTTP_STATUS=$(curl  -w "%{http_code}" -o >(cat >&3) -XPOST 192.168.39.23:9200/_bulk --compressed -# -H 'Content-Type: application/json' --header 'Content-Encoding: gzip' --data-binary @- > /dev/null )
			echo -e "Reponse http : $HTTP_STATUS \n"
			sleep 0.6
		done
		
		((++y))	
	fi
	echo -e "Fichier à enlever :  $x \n"
	echo -e "Reponse http : $HTTP_STATUS \n"
	rm $x 

	echo -e "Fichier supprimé : $x \n"
done


