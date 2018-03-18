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
     * utilisation d’un HTTP post: requests.post (python) pour ajouter les données sur le serveur elasticsearch

# Construction d’un moteur de recherche

- Utilisation de l’application flask comme framework web qui construit un rendu html
- Préparation de query pour chaque table
     * bool: should
     * trouver des phrases ou un simple mot
     * multi_match pour différents fields en même temps
     * pertinence du score
     * agrégations pour le langage
     * normaliser les données en minuscule pour ne pas être sensible à la casse (pendant le mapping) 
     
# Création du Dashboard

- Création de différents graphes
     * nombre de commits par jour pendant un mois (janvier 2018)
     * nombre de commits par jour pendant un mois contenant:
         * repository name
         * language
         * committer name 
     * nombre de commits par seconde pendant 15 minutes
     
# Les problemes

- Le gros volume de données
- Les relations entre les tables
- La transformation des données pour pouvoir les injecter dans elasticsearch

# Conclusion

- Search Engine : [http://34.215.22.13:5000/search](http://34.215.22.13:5000/search)


     
     

