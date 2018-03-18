from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import json

app = Flask(__name__)
es = Elasticsearch('http://192.168.99.100', port=9201)

@app.route('/')
def home():
    return render_template('search.html')

def countLanguages(res):
    xsplit = {}
    for item in res['aggregations']['count']['buckets']:
        dictItem = dict(item)
        x = dictItem['key']
        y = dictItem['doc_count']
        for z in x.split(","):
            if z not in xsplit:
                xsplit[z] = y
            else:
                xsplit[z] += y
           
    dictxSplit = dict(xsplit)
    xjoin = ''            
    for key, value in dictxSplit.items():
        xjoin += '%s(%s); ' % (key,value) 
    return xjoin
    
@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    target = request.form["targettable"]
    res=""
    xjoin =''
    search_term = request.form["input"]
    if target == "Commits":
        res = es.search(
            index="engine-recherche",
            #size=0, 
            body={
                "query": {
                    "bool": {
                        "should": [
                            {"wildcard":{"committer_name": "*" + search_term + "*"}},
                            {"wildcard":{"committer_date": "*" + search_term + "*"}},
                            {"wildcard":{"subject": "*" + search_term + "*"}},
                            {"wildcard":{"message": "*" + search_term + "*"}},
                            {"wildcard":{"repo_name": "*" + search_term + "*"}},
                            {"wildcard":{"language_name": "*" + search_term + "*"}},
                            { 
                                 "bool": {
                                    "should": [
                                        {"match": {"committer_name": {"query": search_term, "type": "phrase"}}},
                                        {"match": {"committer_date": {"query": search_term, "type": "phrase"}}},
                                        {"match": {"subject": {"query": search_term, "type": "phrase"}}},
                                        {"match": {"message": {"query": search_term, "type": "phrase"}}},
                                        {"match": {"repo_name": {"query": search_term, "type": "phrase"}}},
                                        {"match": {"language_name": {"query": search_term, "type": "phrase"}}}
                                    ] 
                                }
                            }
                        ]
                    }                                                                  
                },
                "sort": [
                        { "_score": { "order": "desc" }}                  
                ],
                "aggs": {
                    "count": {
                        "terms" : {"field": "language_name"}
                    }
                }
            }
        )
    else:
        if target == "Contents":
            res = es.search(
                index="contents", 
                #size=0, 
                body={
                    "query": {
                        "bool": {
                            "should": [
                                {"wildcard":{"id": "*" + search_term + "*"}},
                                {"wildcard":{"content": "*" + search_term + "*"}},
                                {"wildcard":{"repo_name": "*" + search_term + "*"}},
                                {"wildcard":{"language_name": "*" + search_term + "*"}},
                                { 
                                    "bool": {
                                        "should": [
                                            {"match": {"id": {"query": search_term, "type": "phrase"}}},
                                            {"match": {"content": {"query": search_term, "type": "phrase"}}},
                                            {"match": {"repo_name": {"query": search_term, "type": "phrase"}}},
                                            {"match": {"language_name": {"query": search_term, "type": "phrase"}}}
                                        ] 
                                    }
                                }
                            ]
                        }                                                                  
                    },
                    "sort": [
                        { "_score": { "order": "desc" }}                  
                    ],
                    "aggs": {
                        "count": {
                            "terms" : {"field": "language_name"}
                        }
                    }
                }
            ) 
    xjoin = countLanguages(res)
    return render_template('results.html', res=res, target=target, xjoin=xjoin)
   
    
if __name__ == '__main__':
        app.secret_key = 'mysecret'
        app.run(host='0.0.0.0',port=5000)