# On va commencer par apprendre à connaître les données évenementielles
# On télécharge une heure de ces données avec:

wget http://data.githubarchive.org/2015-01-01-15.json.gz

# Pour une journée entière: wget http://data.githubarchive.org/2015-01-01-{0..23}.json.gz
# Pour un mois entier: wget http://data.githubarchive.org/2015-01-{01..30}-{0..23}.json.gz

# On se retrouve avec des données zippées. On les dezippe avec:

gunzip -k 2015-01-01-0.json.gz

# -k (=--keep) permet de garder le fichier zippé d'origine

# On va utiliser un notebook pour commencer à comprendre la structure de ces données et savoir
# comment on va pouvoir les analyser
# On utilise un docker-compose avec l'image: jupyter/all-spark-notebook
