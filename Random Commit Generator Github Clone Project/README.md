```html

<h1 style="page-break-before:always; "><b>1. BASE DE DONNÉES</b></h1>
<h1 style="page-break-before:always; "><b>Téléchargement des données pour elasticsearch</b></h1>
<ul>
<li>Utilisation de fichiers de githubarchives
Motivation du choix:</li>
<ul>
<li>Commits</li>
<li>détail des Events</li>
</ul>
<li>Méthode de récupération: </li>
<ul>
<li>Script bash</li>
<h2><i>wget -c http://data.githubarchive.org/{2016..2018}-{01..12}-{01..31}-{0..23}.json.gz</i></h2>
</ul>
</ul>
<h1 style="page-break-before:always; "><b>Parametrage du serveur elasticsearch</b></h1>
<ul>
<li>Docker</li>
<li>kibana</li>
<li>dockerfile</li>
<li>Environnement serveur:</li>
<ul>
<li>Elasticsearch version 6.2</li>
<li>Kibana</li>
<li>Logstash</li>
</ul>
</ul>
<h1 style="page-break-before:always; "><b>Création et indexation de la base de données</b></h1>
<ul>
<li>parametrage d’index github</li>
<li>script d’indexation</li>
<ul>
<li>utilisation de gzip + </li>
<li>REST api d’elasticsearch	</li>
<li>python script : Post par requests</li>
<li>envoi de tranches de 10.000 lignes</li>
<li>création automatique de métadonnées  avant POST</li>
</ul>
</ul>
<h1 style="page-break-before:always; "><b>Calibrage du serveur et mapping</b></h1>
<ul>
<li>reduction nombre de shards</li>
<li>reduction nombre de replicas</li>
<li>remodelage du mapping</li>
<ul>
<li>suppression des nested index avec ignore above qui fait exploser le nombre des fields</li>
<li>creation dynamic templates des mapping</li>
</ul>
<li>augmentation du mapping.total_fields.limit à 2000</li>
</ul>
<h1 style="page-break-before:always; "><b>Calibrage du serveur et mapping (2)</b></h1>
<ul>
<li>Saturation du serveur:</li>
<li>Mapping : limitation des champs text, privilegier les keyword</li>
<li>reindexation avec alias</li>
<li>analyse du mapping </li>
<ul>
<li>par script</li>
<li>par kibana</li>
</ul>
<li>tentative de desindexation des champs se terminant par *url sans repose de l’index</li>
</ul>
<h1 style="page-break-before:always; "><b>2. GÉNÉRATEUR DE COMMITS ET DE FILES ALÉATOIRES</b></h1>
<h1 style="page-break-before:always; "><b>Test de la base, query et calibrage</b></h1>
<ul>
<li>Test d’aggregates sur terms</li>
<ul>
<li>Event types</li>
<li>Repositories</li>
<li>Users</li>
<li>language ...</li>
</ul>
<li>suppression des unassigned_shards</li>
<li>changement de refresh_interval pour booster indexation</li>
<li>dépassement de capacité de stockage au dessus de 80% d’espace libre (88 Gb) - passe en mode readonly, disable_allocation</li>
<li>récupération du mode normal - paramètre : index.routing.allocation.disable_allocation&quot;: False</li>
</ul>
<h1 style="page-break-before:always; "><b>Création et paramétrage serveur web </b></h1>
<ul>
<li>souscription à un serveur web type EC2 amazon AWS</li>
<li>accès SSH avec clé publique partagé </li>
<li>installation serveur flask avec python 2.7</li>
<li>parametrage ouverture des ports 5000 pour all net 0.0.0.0,::/0</li>
<li>installation jupyter notebook  avec ouverture ports 9999 pour all net 0.0.0.0,::/0</li>
<li>installation des librairies pythons nécessaires  </li>
<li>Utilisation de socketio pour afficher les data des POST</li>
<li>Envoi des données sur MQTT</li>
</ul>
<h1 style="page-break-before:always; "><b>Génération aléatoire de commits et files</b></h1>
<ul>
<li>Script en python à partir du serveur elasticsearch</li>
<li>lancement en background process avec nohup</li>
<li>envoi en post des commits aléatoires à partir de la base de donnée elasticsearch</li>
<li>réception et traitement au niveau du serveur web Flask</li>
<li>affichage en temps réel des commits par websockets (limité à 10 lignes puis flush)</li>
<li>transmission du contenu au serveur MQTT avec topic différent selon Repository et Type de Event.</li>
<li>Souscription testée par MQTTFX , client MQTT linux</li>
</ul>
<h1 style="page-break-before:always; "><b>Creation et parametrage serveur MQTT </b></h1>
<ul>
<li>souscription à un serveur web type EC2 amazon AWS</li>
<li>accès SSH avec clé publique partagé </li>
<li>installation docker mqtt eclipse mosquitto, avec publish des ports</li>
<li>parametrage ouverture des ports 1883 et 9001 pour all net 0.0.0.0/::00</li>
<li>tentative de servir en HTTPS websocket en 8000, non concluant pour un test connection HIVEMQTT web client</li>
</ul>
<h1 style="page-break-before:always; "><b>CONCLUSION</b></h1>
<ul>
<li>Elasticsearch : <a href="http://88.169.46.187:9200/"><u>http://88.169.46.187:9200/</u></a></li>
<li>Kibana : <a href="http://88.169.46.187:9200/"><u>http://88.169.46.187:5601/</u></a></li>
<li>Serveur web : <a href="http://34.215.22.13:5000/"><u>http://34.215.22.13:5000/</u></a></li>
<li>Serveur MQTT : 18.188.23.129:1883</li>
</ul>



```
