```html

# 1. BASE DE DONNÉES

# Téléchargement des données pour elasticsearch

- Utilisation de fichiers de githubarchives
Motivation du choix:

- Commits
- détail des Events

- Méthode de récupération: 

- Script bash

## wget -c http://data.githubarchive.org/{2016..2018}-{01..12}-{01..31}-{0..23}.json.gz

# Parametrage du serveur elasticsearch

- Docker
- kibana
- dockerfile
- Environnement serveur:

- Elasticsearch version 6.2
- Kibana
- Logstash

# Création et indexation de la base de données

- parametrage d’index github
- script d’indexation

- utilisation de gzip + 
- REST api d’elasticsearch	
- python script : Post par requests
- envoi de tranches de 10.000 lignes
- création automatique de métadonnées  avant POST

# Calibrage du serveur et mapping

- reduction nombre de shards
- reduction nombre de replicas
- remodelage du mapping

- suppression des nested index avec ignore above qui fait exploser le nombre des fields
- creation dynamic templates des mapping

- augmentation du mapping.total_fields.limit à 2000

# Calibrage du serveur et mapping (2)

- Saturation du serveur:
- Mapping : limitation des champs text, privilegier les keyword
- reindexation avec alias
- analyse du mapping 

- par script
- par kibana

- tentative de desindexation des champs se terminant par *url sans repose de l’index

# 2. GÉNÉRATEUR DE COMMITS ET DE FILES ALÉATOIRES

# Test de la base, query et calibrage

- Test d’aggregates sur terms

- Event types
- Repositories
- Users
- language ...

- suppression des unassigned_shards
- changement de refresh_interval pour booster indexation
- dépassement de capacité de stockage au dessus de 80% d’espace libre (88 Gb) - passe en mode readonly, disable_allocation
- récupération du mode normal - paramètre : index.routing.allocation.disable_allocation": False

# Création et paramétrage serveur web 

- souscription à un serveur web type EC2 amazon AWS
- accès SSH avec clé publique partagé 
- installation serveur flask avec python 2.7
- parametrage ouverture des ports 5000 pour all net 0.0.0.0,::/0
- installation jupyter notebook  avec ouverture ports 9999 pour all net 0.0.0.0,::/0
- installation des librairies pythons nécessaires  
- Utilisation de socketio pour afficher les data des POST
- Envoi des données sur MQTT

# Génération aléatoire de commits et files

- Script en python à partir du serveur elasticsearch
- lancement en background process avec nohup
- envoi en post des commits aléatoires à partir de la base de donnée elasticsearch
- réception et traitement au niveau du serveur web Flask
- affichage en temps réel des commits par websockets (limité à 10 lignes puis flush)
- transmission du contenu au serveur MQTT avec topic différent selon Repository et Type de Event.
- Souscription testée par MQTTFX , client MQTT linux

# Creation et parametrage serveur MQTT 

- souscription à un serveur web type EC2 amazon AWS
- accès SSH avec clé publique partagé 
- installation docker mqtt eclipse mosquitto, avec publish des ports
- parametrage ouverture des ports 1883 et 9001 pour all net 0.0.0.0/::00
- tentative de servir en HTTPS websocket en 8000, non concluant pour un test connection HIVEMQTT web client

# CONCLUSION

- Elasticsearch : [http://88.169.46.187:9200/](http://88.169.46.187:9200/)
- Kibana : [http://88.169.46.187:5601/](http://88.169.46.187:9200/)
- Serveur web : [http://34.215.22.13:5000/](http://34.215.22.13:5000/)
- Serveur MQTT : 18.188.23.129:1883

```
