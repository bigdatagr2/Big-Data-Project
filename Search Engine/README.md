# Téléchargement des données

- Utilisation de Google Cloud BigQuery

- Récupération des données: 
    * Projet: bigquery-public-data
    * Dataset: github_repos
    * Tables: commits, contents, files, languages
    * Téléchargement au format json

# Creation du Dataset

- Choix de plusieurs repository:
    * tensorflow/tensorflow
    * facebook/react
    * twbs/bootstrap
    * apple/swift
    * Microsoft/vscode
    * torvalds/linux
    
- Relation entre les tables:
    * commits - languages
    * contents - files - languages (binary = false)

# Elasticsearch

- Création d’un mapping dynamique pour contrôler le type de chaque field:
    * date_detection: true
    * numeric_detection: true
    * dynamic_templates: 
        * path_match (name, date)
- Preparation des données:
    * metadata: 
    {"_index": "bigdata-commits", "_type":"data", "_id": i}
    * data: 
	 {"field1": "valeur1", "field2":"valuer2", "filed3": “valeur3”,…-     

- Indexation du dataset:
     * _bulk
     * limite d’indexation de 10000 lignes
     + utilisation d’un HTTP post: requests.post (python) pour ajouter les données sur le serveur elasticsearch
