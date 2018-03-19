# To begin: know event data
## Load one hour of these data with:

```
wget http://data.githubarchive.org/2015-01-01-15.json.gz
```

For a day:
```
wget http://data.githubarchive.org/2015-01-01-{0..23}.json.gz
```
For a month:
```
wget http://data.githubarchive.org/2015-01-{01..30}-{0..23}.json.gz
```

## Must unzip these loaded files (one file by hour) with:
```
gunzip -k 2015-01-01-0.json.gz
```
-k (=--keep) must be used to keep the original zip file

Use a notebook to understand the structure of data and to have an idea to analyze them
Use a docker-compose with image: jupyter/all-spark-notebook

# To download necessary data
 1. download one month of event data
 2. In a loop in R program:
   - unzip one file
   - transform in dataframe
   - select columns
   - append with the previous selection
   - remove unzip file
3.  save the final dataset in csv

# To compute stats about this data
